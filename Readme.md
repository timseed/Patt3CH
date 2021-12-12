# RBN Pattern

This project is to try and allow me, to understand how the file that appears to be quite critical to the CW Skimmer process is configured/handled.

## Current status of patt3ch.lst

This file has been added to, modded, and adjusted for a long while. So much so that it is not especially consistent, has some overlaps (Oman, UAE for example) and is not very well understood.

## Basic function of patt3ch.lst

The CW Skimmer produces letters, digits and '/' symbols (I am not aware of anything else), on it's interpretation of I/Q data. In a perfect world, all signals would have been sent, modulated and received clearly. But sadly this is rarely the case... and mistakes in the 'interpretation' of the I/Q data are to be expected.

So with a text stream for say 14.020 ... containing 

    AA1 B1B C3C M0FGC 4DD1A EE FF 
    
 How does a computer detect the call sign(s) ?
 
 It uses template(s)
 
 ## Templates 
 
 In computing templates are very commonly used in some programming languages to find and extract data. And the most popular/common template is the Regular Expression (RegEx).
 
 Patt3Ch.lst uses an variant of a RegEx.
 
 # How to improve Patt3ch.lst ?
 
 I believe some form of SDLC (System development life cycle) should be undertaken such as 
 
   - Understand
   - Analyze
   - Model
   - Verify 
   - Issue
   
 ## Understand
 
 The RBN-OPS group has recently had a large discussion on this format and some of the **extras** are now being understood.
 
 ## Analyze 
 
 The code in this project, aims to accomplish this.
 
 ## Model
 
 If we create a new version of Patt3ch.lst, we should be able to pass a decent set of known ham callsigns against it, and check if they are detected or not.
 
 Whilst there is not 1 data source for this, a combination of RBN data files, plus Super-Check-Partial (SCP) will give an initial (CW bias) data set.
 
 ## Verify 
 
 A simple process taking the new rule file, and a callsign data file.
 
 # File Format
 
 Patt3ch.lst looks like this (I am using a subset of the Philippines callsign group)
 
 ```text
+ DU4@@
  DU4@@@
  DU5@@@
  DU6#@@@
 ```

This is what things mean

  - '#' This means [0-9]
  - '@' This means [A-Za-z]
  - '+' This is a frequent grouping, it does not need to be seen often, before it is reported. 
  
So if a callsign of *DU4AA* is seen say 3 times... it will be output, but a call of *DU4ABC* may need 4 or 5 times to be seen before being output.

If a call of 'DU41AA' is seen 5 time... it will not be output as it does not match the **template**.

But a call of 'DU66ZZZ' does match, but 'DU6ZZ' does not match.

It is important you understand these rules...


## Rule generation Clarification


### My intial understanding 

Initially when I write  the first code, I converted all calls to their templates, and then simplified the templates.

call |  template |
-----|-----------|
AB1AA     |  @@#@@  |
DU3TW   | @@#@@ | 
K1AB    | @#@@  |

So the 'unique' templates are only 2

  -  @@#@@  
  -   @#@@ 

### 3 letter requirement - Invalid

After some more discussion on RBN-OPS, it seemed that the first 3 Letters were needed

call |  template |
-----|-----------|
AB1AA     |  AB1@@  |
DU3TW   | DU3@@ | 
K1AB    | K1A@  |

So the size of the templates increased - but not by too much surprisingly.

**This mechanism is now aparently invalid**


### Clarified format.


From the autor VE3NEA 

```text
If the call starts with letter-digit-letter, 
then only the first two characters are kept explicit, 
so the pattern of N4ZR is N4@@. 

If the call starts with digit-letter-letter, 
then 4 characters are kept, 
so the pattern of 3DA0RU is 3DA0@@.
```

So with that rule explained, I have re-implemented the PatternBuilder, incorporating a count of the template - this is used to generate the + pro-sign on the lines.


# Running / Testing

There is a Makefile supplied, but this expects a Python Virtual Env called *pe39* to be installed. So you need to create your own virtual Env, and update the Makefile.

## Python Requirements

There is only 1 extra module required, Pandas. To install this

	*Switch to your Python Virtual Env*
	pip install pandas

If you want to visualize pandas development, I suggest you install *jupyter notebook*. 


## Build Pattern definitions

So with Pandas installed, you want to try *build patterns*

	make buildmasterplus

This should output something like this


```text
Running
Checking pattern file MASTERPLUS.SCP
Loading MASTERPLUS.SCP
Length 0 mean is 96.74572127139365 std 795.5450584887159
common_as_list has 72 records
file format0.lst has 409 records
Length 1 mean is 52.618351063829785 std 168.76468014956737
common_as_list has 139 records
file format1.lst has 752 records
Length 2 mean is 20.11642094560244 std 50.10133342728507
common_as_list has 421 records
file format2.lst has 1967 records
Length 3 mean is 6.879172461752434 std 18.322565362721676
common_as_list has 1065 records
file format3.lst has 5752 records
Length 4 mean is 2.080826672275978 std 8.580382842822866
common_as_list has 2265 records
file format4.lst has 19016 records
```
The time to produce this is sub 3 seconds....

The number of rules per 'length' of the prefix... is 

    - 0   409 format0.lst
    - 1   752 format1.lst
    - 2  1967 format2.lst
    - 3  5752 format3.lst
    - 4 19016 format4.lst

My source records which I created these rules had 39,000 records in. So this is quite a useful and reasonable compression.

## Validate the Pattern 

So with the pattern file (say format3.lst) - we re-run the Source data... i.e. we simulate receiving these callsigns, what will the percentage of success/failure be.

o do this we use (make of course)

     make test3p
     
This now takes a little longer... Note: Python and RegEx's are quite slow even if they are compiled. But this is not too important, it is the validation of the pattern file that is the primary objective.

At the bottom of the screen ... I see 

```text
We have 5752 rules
We have 361 unmatched rules
rule match percentage is 93.724 %
We have 0 unmatched calls from SCP
call match percentage is 100.000%
of which 0 has a /
```

So every call in our test data set... was matched (let's not talk about overfitting just now); And we only have 361 un-used rules.

For the moment that looks ok.

## Visually check the pattern file

I only really understand call prefixes from where I have been licenced... 


### Oman A4 Check

So checking on Oman (A4)

```text
  A41@@
  A42@
  A44@
  A45@@
  A47@@
  A4@@
```
That looks correct. Non have been marked as commonly occurring.

### Philippines (DU only)

So checking for DU prefixes (Sorry 4D3 people),

```text
  DU1/@#@@@
  DU1@
+ DU1@@
+ DU1@@@
  DU2@@
  DU3#@
  DU3@
+ DU3@@
  DU3@@@
  DU4@@
  DU4@@@
  DU6/@#@@
  DU6@@
  DU7@
  DU7@@@
  DU8@@
  DU9@@@
```

Here I see three classes of frequently heard prefixes... (DU1@@, DU1@@@) - this is Manila standard and vanity calls, and my own region (3) with the prefix (DU3@@).

These areas are generally the most populus in terms of ham operators using the DU prefix.

#To Do

  - Wrap into a Python Package.
  - Add new call-sign sources.
  - Test using different Data sets
    - RTTY/FT8 Contest data - if available
   
  




   
 
