# fsbuddy

## Description
Welcome to File System Buddy!

This is a CLI tool meant to make file system operations easy to use and intuitive.

## Installation
Installing is as simple as:

1. Open terminal or shell, `cd ~`
2. `git clone https://github.com/richyuh/fsbuddy.git`
3. `pip install ./fsbuddy`

## Usage
The following operations are available:

1. `fsbuddy size [path]`  
   Get the total size of the specified path.

2. `fsbuddy list [path] [--size] [--date]`  
   List the files and subdirectories in the specified path.  
   - `--size`: Sort by file size in descending order.  
   - `--date`: Sort by last access date in descending order.

3. `fsbuddy delete [path]`  
   Delete the specified file or directory.

## Constraints
1. macOS/linux only
2. best effort - skips paths with permissions issues
