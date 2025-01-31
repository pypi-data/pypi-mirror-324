# aliceCSV -- Simple and Cross-Platform CSV Module

[中文版 / Chinese Version](/README-zh.md)

**aliceCSV** is a simple, user-friendly, and cross-platform CSV module.

This module allows you to operate **CSV files as two-dimensional tables** easily and convert them into other formats with minimal effort. It is lightweight, has no dependencies, and is more intuitive compared to the built-in CSV libraries in Python and other languages.

------

## Overview

aliceCSV is a cross-platform and cross-language CSV parsing software. It simplifies handling CSV files in software development by converting them into universal 2D arrays/lists. The module includes **error correction** and **format conversion** capabilities.

The software is implemented in **C++**, **Python**, and **JavaScript**, corresponding to use cases in embedded systems and applications, data processing, and web front-end development, which covered most development needs.

The software has the capability to handle non-standard CSV files and is optimized for common errors encountered when handling CSV files. It strives to **restore the original intent of the author** when a file contains formatting errors.

------

## Features

In addition to being simple and easy to use, one of aliceCSV's major features is its **strong compatibility with CSV files that do not conform to RFC 4180 or have formatting errors.**

For example, if there is a file named "sheet.csv" with the following content:

```
avc,"She said,"I like orange juice.""
```

This is a common mistake.

According to Section 7 in RFC 4180, this expression is incorrect because the double quotes in the second field must be escaped with another double quote. The correct content should be:

```
avc,"She said,""I like orange juice."""
```

If you open this malformed CSV file in Excel, it will be interpreted as:

| avc  | She said,I like orange juice."" |
| ---- | ------------------------------- |
|      |                                 |

However, aliceCSV can correctly interpret the author's original intent.

```python
from aliceCSV import *
myFile = open("sheet.csv", encoding="utf-8")
print(parseCSV(myFile))
```

It will output the following result:

> [['avc', 'She said,"I like orange juice."']]

Don't worry if this compatibility will affect normal parsing—take the above Excel example. If you want to express the incorrect result shown by Excel, you shouldn't use such a wrong format in the first place. This kind of ambiguous format can only be guessed by the parsing program, and the result depends on the text and the interpretation program used, which is uncertain.

aliceCSV just chooses to output the result that is most likely the author's true intention based on common mistakes.

------

## Installation

### Python

You can use pip to install it:

```
pip install aliceCSV
```

Or download it from this repository.

------

### C++

Download the cpp files provided in this repository.

------

### JavaScript

Use the `aliceCSV_1.0.1.js` file provided in this repository.

------

## How to Use

------

### 1. Parse CSV Content into a Two-Dimensional List

```
parseCSV(csv_text, [optional]delimiter)
```

> `csv_text`: The text of the CSV file to be parsed.
> `delimiter`: The delimiter of the CSV file. Optional, default is `","`.

![image-20241221164314904](assert/1-1.png)

**Warning:**

If you encounter issues processing CSV files like this one, it might be due to an extra space following the delimiter `","`. In such cases, the actual delimiter would be `", "`.

```
name, gender, height, address
John, male, 175cm, "123 Main Street, New York, USA"
Emily, female, 160cm, "45 Oxford Road, London, UK"
Michael, male, 180cm, "10 Rue de la Paix, Paris, France"
Sophia, female, 165cm, "25 Alexanderplatz, Berlin, Germany"
```

You can learn more about it in  [**5. Format Conversion**](#5. Format Conversion).

------

### 2. Parse a Specific Line of a CSV File

Users can use the `parseLine` function to parse a specific line of a CSV file.

```
parseLine(line, delimiter)
```

> `line`: The text of a specific line in the CSV file.
> `delimiter`: The delimiter to use during parsing. Optional, default is `","`.

------

### 3. Write a Table to a CSV File

The `writeCSV` function can save a table represented as a two-dimensional list into a CSV file.

![image-20241221164739331](assert/3-1.png) 

**Note: Due to differences in I/O operations across programming languages, there are slight differences among implementations:**

**In the Python and C++ implementations, the `writeCSV` function will write directly to the disk.**

**But in JavaScript one, it returns a blob object representing the CSV file.**



The parameters required for the function and their meanings are as follows:

```
writeCSV(sheet, [optional]output_path, [optional]delimiter, [optional]sheet_encoding, [optional]line_break)
```

> `sheet`: The two-dimensional list to be saved.
> `output_path`: The output path. Optional, default is creating `"output.csv"` in the current directory.
> `sheet_encoding`: The encoding format of the output file. Optional, default is `"utf-8"`.
> `delimiter`: The delimiter used in the CSV file. Optional, default is `","`.
> `line_break`: The line break style used in the output file. Optional, default is `"\n"`.

------

### 4. Fix Length Issues in CSV Files

For various reasons, some CSV files may have rows with varying numbers of fields, which does not conform to the common RFC 4180 standard and may cause issues in certain scenarios. Users can use the `fixLineLength` function to make all rows have the same number of fields.

The parameters required for the function and their meanings are as follows:

```
fixLineLength(csv_sheet)
```

> `csv_sheet`: The table represented as a two-dimensional list.

For example, consider a table where rows have different lengths:

![image-20241221165142136](assert/4-1.png) 

You can use `fixLineLength` to fix it:

![image-20241221165155778](assert/4-2.png)

Save the result as a CSV file and open it. You will see that each row now has the same number of fields.

![image-20241221165203548](assert/4-3.png) 

------

### 5. Format Conversion

The `fixCSV` function can save CSV files in various compatible formats, including changing the delimiter, file encoding, line break style, etc.

For example, for a CSV file with a delimiter of `"."`, you can use the `fixCSV` function to convert it into a commonly used CSV file with commas as the delimiter.

![image-20241221165533896](assert/5-1.png) 

As shown, using the Python implementation of the `fixCSV` function, input the source file path and source file delimiter to output the converted `"output.csv"` file in the current path.

![image-20241221165542191](assert/5-2.png) 

**Note: Due to variations in the logic of I/O operations across programming languages, implementations may differ slightly.**

**In the JavaScript implementation, the `fixCSV` function returns a Promise, and users can resolve this Promise to obtain a blob object representing the converted file.**



The function requires two parameters for simple conversion. More parameters can be added as needed.

```
fixCSV(path, [optional]output_path, [optional]origin_delimiter, [optional]target_delimiter, [optional]origin_encoding)
```

> `path`: The path to the input CSV file.   
>
> `output_path`: The path to the generated CSV file. Optional, defaults to `"output.csv"`. This parameter is not available in the JavaScript implementation.    
>
> `origin_delimiter`: The delimiter used in the original CSV file. Optional, defaults to `","`.    
>
> `target_delimiter`: The delimiter to be used in the output file. Optional, defaults to `","`.  
>
> `origin_encoding`: The encoding of the original file. Optional, defaults to `"utf-8"`.   
>
> `target_encoding`: The encoding to be used in the output file. Optional, defaults to `"utf-8"`.  
>
>  `target_line_break`: The line break style for the output file. Optional, defaults to `"\n"`.  



------

## License

This project originated from [aliceCSV v0.1.3](https://github.com/Alice-Drop/aliceCSV).

The aliceCSV code in this repository is licensed under the MIT License. Please refer to the `LICENSE` file for details.