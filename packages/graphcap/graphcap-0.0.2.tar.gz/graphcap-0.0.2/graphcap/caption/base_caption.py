"""
# SPDX-License-Identifier: Apache-2.0
Base Caption Module

Provides base classes and shared functionality for different caption types.
"""

import asyncio
import json
import shutil
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table
from tqdm.asyncio import tqdm_asyncio

from ..providers.clients.base_client import BaseClient
from ..schemas.structured_vision import StructuredVisionConfig

# Initialize Rich console
console = Console()


def pretty_print_caption(caption_data: Dict[str, Any]) -> str:
    """Format caption data for pretty console output."""
    return json.dumps(caption_data["parsed"], indent=2, ensure_ascii=False)


class BaseCaptionProcessor(ABC):
    """
    Base class for caption processors.

    Provides shared functionality for processing images with vision models
    and handling responses. Subclasses implement specific caption formats.

    Attributes:
        config_name (str): Name of this caption processor
        version (str): Version of the processor
        prompt (str): Instruction prompt for the vision model
        schema (BaseModel): Pydantic model for response validation
    """

    def __init__(
        self,
        config_name: str,
        version: str,
        prompt: str,
        schema: type[BaseModel],
    ):
        self.vision_config = StructuredVisionConfig(
            config_name=config_name,
            version=version,
            prompt=prompt,
            schema=schema,
        )

    def _sanitize_json_string(self, text: str) -> str:
        """
        Sanitize JSON string by properly escaping control characters.

        Args:
            text: Raw JSON string that may contain control characters

        Returns:
            Sanitized JSON string with properly escaped control characters
        """
        # Define escape sequences for common control characters
        control_char_map = {
            "\n": "\\n",  # Line feed
            "\r": "\\r",  # Carriage return
            "\t": "\\t",  # Tab
            "\b": "\\b",  # Backspace
            "\f": "\\f",  # Form feed
            "\v": "\\u000b",  # Vertical tab
            "\0": "",  # Null character - remove it
        }

        # First pass: handle known control characters
        for char, escape_seq in control_char_map.items():
            text = text.replace(char, escape_seq)

        # Second pass: handle any remaining control characters
        result = ""
        for char in text:
            if ord(char) < 32:  # Control characters are below ASCII 32
                result += f"\\u{ord(char):04x}"
            else:
                result += char

        return result

    @abstractmethod
    def create_rich_table(self, caption_data: Dict[str, Any]) -> Table:
        """
        Create a Rich table for displaying caption data.

        Args:
            caption_data: The caption data to format

        Returns:
            Rich Table object for display
        """
        pass

    @property
    def supported_formats(self) -> List[str]:
        """List of supported output formats for this processor."""
        return []

    def write_format(self, format_name: str, job_dir: Path, caption_data: Dict[str, Any]) -> None:
        """
        Write caption data in a specific format.

        Args:
            format_name: Name of the format to write
            job_dir: Directory to write the output to
            caption_data: Caption data to format and write
        """
        pass

    async def process_single(
        self,
        provider: BaseClient,
        image_path: Path,
        max_tokens: Optional[int] = 4096,
        temperature: Optional[float] = 0.8,
        top_p: Optional[float] = 0.9,
        repetition_penalty: Optional[float] = 1.15,
    ) -> dict:
        """
        Process a single image and return caption data.

        Args:
            provider: Vision AI provider client instance
            image_path: Path to the image file
            max_tokens: Maximum tokens for model response
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter

        Returns:
            dict: Structured caption data according to schema

        Raises:
            Exception: If image processing fails
        """
        try:
            completion = await provider.vision(
                prompt=self.vision_config.prompt,
                image=image_path,
                schema=self.vision_config.schema,
                model=provider.default_model,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                repetition_penalty=repetition_penalty,
            )

            # Handle response parsing with sanitization
            if isinstance(completion, BaseModel):
                result = completion.choices[0].message.parsed
                if isinstance(result, BaseModel):
                    result = result.model_dump()
            else:
                result = completion.choices[0].message.parsed
                # Handle string responses that need parsing
                if isinstance(result, str):
                    sanitized = self._sanitize_json_string(result)
                    try:
                        result = json.loads(sanitized)
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse sanitized JSON: {e}")
                        raise
                elif "choices" in result:
                    result = result["choices"][0]["message"]["parsed"]["parsed"]
                elif "message" in result:
                    result = result["message"]["parsed"]

            return result
        except Exception as e:
            raise Exception(f"Error processing {image_path}: {str(e)}")

    async def process_batch(
        self,
        provider: BaseClient,
        image_paths: List[Path],
        max_tokens: Optional[int] = 4096,
        temperature: Optional[float] = 0.8,
        top_p: Optional[float] = 0.9,
        max_concurrent: Optional[int] = 5,
        repetition_penalty: Optional[float] = 1.15,
        output_dir: Optional[Path] = None,
        store_logs: bool = False,
        formats: Optional[List[str]] = None,
        copy_images: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Process multiple images and return their captions.

        Args:
            provider: Vision AI provider client instance
            image_paths: List of paths to image files
            max_tokens: Maximum tokens for model response
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            max_concurrent: Maximum number of concurrent API requests
            output_dir: Directory to store incremental results and job info
            store_logs: Whether to store logs in the output directory
            formats: List of additional formats to write caption data
            copy_images: Whether to copy images to the output directory

        Returns:
            List[Dict[str, Any]]: List of caption results with metadata
        """
        # Create job directory with timestamp if output_dir provided
        job_dir = None
        job_output = None
        job_info = None
        log_file = None

        if output_dir:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            job_dir = output_dir / f"batch_{timestamp}"
            job_dir.mkdir(parents=True, exist_ok=True)

            # Create output file and job info
            job_output = job_dir / "captions.jsonl"
            job_info = job_dir / "job_info.json"

            # Configure logging if requested
            if store_logs:
                log_file = job_dir / "process.log"
                # Add file logger while keeping console output
                logger.add(
                    log_file,
                    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
                    level="INFO",
                    rotation="100 MB",
                )

            # Write initial job info
            job_info_data = {
                "started_at": timestamp,
                "provider": provider.name,
                "model": provider.default_model,
                "config_name": self.vision_config.config_name,
                "version": self.vision_config.version,
                "total_images": len(image_paths),
                "sampling": {
                    "original_count": getattr(image_paths, "original_count", len(image_paths)),
                    "sample_size": getattr(image_paths, "sample_size", len(image_paths)),
                    "sample_method": getattr(image_paths, "sample_method", "all"),
                },
                "params": {
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": top_p,
                    "max_concurrent": max_concurrent,
                    "repetition_penalty": repetition_penalty,
                },
                "log_file": str(log_file.relative_to(job_dir)) if log_file else None,
                "formats": formats or [],
                "copy_images": copy_images,
            }
            job_info.write_text(json.dumps(job_info_data, indent=2))

            # Copy images if requested
            if copy_images:
                images_dir = job_dir / "images"
                images_dir.mkdir(exist_ok=True)
                for path in image_paths:
                    try:
                        shutil.copy2(path, images_dir / path.name)
                    except Exception as e:
                        logger.error(f"Failed to copy image {path}: {e}")

        logger.info(f"Processing {len(image_paths)} images with {provider.name} provider")
        logger.info(f"Using max concurrency of {max_concurrent} requests")
        if job_dir:
            logger.info(f"Writing results to {job_dir}")
            if log_file:
                logger.info(f"Logging to {log_file}")

        semaphore = asyncio.Semaphore(max_concurrent)
        active_requests = 0
        processed_count = 0
        failed_count = 0

        async def process_with_semaphore(path: Path) -> Dict[str, Any]:
            nonlocal active_requests, processed_count, failed_count

            async with semaphore:
                try:
                    active_requests += 1
                    logger.info(f"Starting request for {path.name} (Active requests: {active_requests})")

                    result = await self.process_single(
                        provider=provider,
                        image_path=path,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                        repetition_penalty=repetition_penalty,
                    )

                    active_requests -= 1
                    processed_count += 1
                    logger.info(f"Completed request for {path.name} (Active requests: {active_requests})")

                    caption_data = {
                        "filename": f"./{path.name}",
                        "config_name": self.vision_config.config_name,
                        "version": self.vision_config.version,
                        "model": provider.default_model,
                        "provider": provider.name,
                        "parsed": result,
                    }

                    # Write result incrementally if output file exists
                    if job_output:
                        with job_output.open("a") as f:
                            f.write(json.dumps(caption_data) + "\n")

                        # Update job info
                        job_info_data["processed_count"] = processed_count
                        job_info_data["failed_count"] = failed_count
                        job_info_data["completed_at"] = datetime.now().strftime("%Y%m%d_%H%M%S")
                        job_info.write_text(json.dumps(job_info_data, indent=2))

                    # Create and display Rich table
                    console.print(f"\n[bold cyan]Processed {path.name}:[/bold cyan]")
                    table = self.create_rich_table(caption_data)
                    console.print(table)

                    # Write additional formats if requested
                    if formats:
                        for fmt in formats:
                            if fmt in self.supported_formats:
                                self.write_format(fmt, job_dir, caption_data)

                    return caption_data
                except Exception as e:
                    active_requests -= 1
                    failed_count += 1
                    logger.error(f"Failed request for {path.name} (Active requests: {active_requests})")
                    error_data = {
                        "filename": f"./{path.name}",
                        "config_name": self.vision_config.config_name,
                        "version": self.vision_config.version,
                        "model": provider.default_model,
                        "provider": provider.name,
                        "parsed": {"error": str(e)},
                    }

                    # Write error result if output file exists
                    if job_output:
                        with job_output.open("a") as f:
                            f.write(json.dumps(error_data) + "\n")

                        # Update job info
                        job_info_data["processed_count"] = processed_count
                        job_info_data["failed_count"] = failed_count
                        job_info_data["completed_at"] = datetime.now().strftime("%Y%m%d_%H%M%S")
                        job_info.write_text(json.dumps(job_info_data, indent=2))

                    console.print(f"\n[bold red]Failed to process {path.name}:[/bold red] {str(e)}")
                    return error_data

        results = await tqdm_asyncio.gather(
            *[process_with_semaphore(path) for path in image_paths],
            desc=f"Processing images with {provider.name}",
        )

        # Log summary with Rich
        success_count = sum(1 for r in results if "error" not in r["parsed"])
        summary_table = Table(title="Processing Summary", show_header=False)
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="green")
        summary_table.add_row("Total Images", str(len(results)))
        summary_table.add_row("Successful", str(success_count))
        summary_table.add_row("Failed", str(len(results) - success_count))

        console.print("\n")
        console.print(summary_table)

        return results
