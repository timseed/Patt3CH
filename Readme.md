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




   
 