# FastFetch: Parallel Image Downloader

## Project Overview

FastFetch is a production-style image downloading system built in Python. 
The program downloads 100 images from:

https://picsum.photos/300

This project demonstrates the difference between serial and parallel execution models while implementing:

- Controlled concurrency (maximum 5 workers)
- Thread-safe logging using a mutex (Lock)
- Retry logic (up to 3 attempts)
- Timeout handling
- Failure resilience (program never crashes)
- Real-time progress monitoring
- Performance benchmarking

The goal is to simulate a reliable, production-grade downloading pipeline similar to real-world web scraping and distributed ingestion systems.

---

## Problem Description

Downloading large numbers of remote resources introduces several engineering challenges:

- Requests may hang indefinitely
- Network calls may fail
- Multiple threads may corrupt shared files
- Systems must avoid overwhelming external services
- Execution time should be optimized

This project addresses those challenges using structured concurrency, error handling, rate limiting, and thread-safe logging.

---

## Setup Instructions

Clone the repository and create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests certifi
```

Once you do this to run the code you must run the following:

```
python3 generate_image_urls.py
 // the images will be saved into req1_generate_100_imageurls

 python3 serial_image_downloader.py
 // the images will be saved into req2_serial_downloader_100urls

 python3 parallel_image_downloader.py
 // the images will be saved into req3_parallel_downloader_100urls/
 ```

 ## Serial vs Parallel Execution

 ## Serial Version

Downloads images sequentially (one at a time)

Waits for each request to complete before starting the next

Simple execution model

Slower overall runtime

Measured execution time:

11.88 seconds

## Parallel Version

Uses ThreadPoolExecutor

Runs up to 5 downloads simultaneously

Rate-limited to prevent overloading the service

Thread-safe logging via threading.Lock

Handles retries and timeouts gracefully

Measured execution time:

2.37 seconds

## Why Parallel is Faster

Image downloading is an I/O-bound task, meaning most of the time is spent waiting for network responses.

In the serial version:

The program waits for each image to download before starting the next one.

In the parallel version:

While one request is waiting for a response, other threads can start additional downloads.

This overlapping of network waiting time drastically reduces total runtime.

Parallel execution achieved approximately a 5x speed improvement.

## Performance Results
Serial	11.88
Parallel	2.37
Speedup achieved through controlled multithreading.

## Logging

All download attempts are logged in logger.txt

Possible statuses include:

SUCCESS

TIMEOUT

FAILED

RETRY 1

RETRY 2

TIMEOUT | FAILED

Thread-safe logging is implemented using a mutex (threading.Lock) to prevent race conditions when multiple threads write to the log file simultaneously.

## Design Decisions
1. ThreadPoolExecutor

Used instead of manually creating threads because:

It cleanly limits the number of workers (max_workers=5)

Simplifies concurrency management

Improves readability and maintainability

Automatically handles thread lifecycle

2. Mutex (threading.Lock)

Multiple threads write to logger.txt.
Without synchronization, log entries could become corrupted or interleaved.

3. Retry Logic

Each failed download:

Retries up to 3 times

Logs each retry attempt

Marks FAILED after the final attempt

This improves reliability and mimics real-world fault-tolerant systems.

4. Timeout Handling

Each request has a 3-second timeout to prevent hanging connections.

If a timeout occurs:

It is logged

The program retries (up to 3 times)

Execution continues safely

This ensures the program never stalls indefinitely.

5. Failure Isolation

Each download runs inside its own try/except block.

If one download fails:

It does not terminate the program

Other downloads continue

The final report reflects total successes and failures