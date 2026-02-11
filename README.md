# Production Project - George Wilkinson C33680193

The purpose of this project is to highlight the accessibility boundaries within university booking systems and to produce a prototype that can improve awareness so that its functional for all participants. 

To understand the type of issues that impact student particpation when naviagting these systems, research will be conducted across official documentation, published research and case studies. 

Tools such as WAVE (Web Accessibility Evaluation Tool) (https://wave.webaim.org/) will be used to evaulate disability awareness when operating the booking systems. 

The end goal is to produce a prototype that can improve accessibility for all users and this version of the booking system will aim to meet that goal. 


## Understanding the functionality of WAVE
WAVE is a free browser extension used to measure page accessibility issues on users with diabilities. The extension uses an in-built scoring system called Accessibility IMpact (AIM) which reports on:
1. Number of detectable errors
2. Error density (number of detectable errors by page elements)
3. Number of WAVE alerts (possible or likely accessibility issues)

It provides a comparitive score from 1 to 10, 10 being highly accessible and 5 indicating the page is roughly average compared to other web pages. 

When WAVE is activated on the chosen web page it will show a 'details' panel of the following detectable elements:
- Errors: These represent critical accessibility issues that need to be fixed. For example, missing alternative text on images is a common error. Alt text is essential for screen readers to describe the content of an image to visually impaired users.
- Contrast Errors: These indicate specific types of accessibility errors related to color contrast. These should also be prioritised and fixed.
- Alerts: These could be accessibility issues. They should be checked to see if they are or not.
- Features: These highlight existing accessibility features that WAVE detects. Things like proper use of headings or accessible form labels are marked as features.
- Structure: These show the semantic structure of your webpage, such as headings, landmarks, and other HTML5 elements that help organise content logically.
- ARIA: These indicate the correct and incorrect ARIA usage of the page, such as missing labels or misused roles. Most ARIA items require a manual review to see if they’re used properly.

## How to use WAVE
1. Download the WAVE tool to use as an extension.
2. Load up https://becbookings.leedsbeckett.ac.uk/ and go to the 'booking' page where there is a list of equipment. 
3. Open the WAVE extension and it'll show a detailed accessibility panel.

## How to use WAVE for the prototype
1. Cloan the URL of the project to PyCharm as the chosen IDE.
2. At this current time of documenation, pages are static HTML so open one of the HTML files via the broswer support function (Choose the one with the WAVE tool).
3. The page will load and run the WAVE tool.


## Current software version
- Django 6.0
- PyCharm 2025.2.5
- Font Awesome 7.0.0
- Bulma 1.0.3
