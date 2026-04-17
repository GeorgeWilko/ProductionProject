# Production Project - George Wilkinson C33680193

## Table of Contents
- [Background Information](#background-information)
- [Project Features](#project-features)
- [Understanding the functionality of WAVE](#understanding-the-functionality-of-wave)
- [How to use WAVE](#how-to-use-wave)
- [How to use WAVE for the prototype](#how-to-use-wave-for-the-prototype)
- [Pre-requisites](#pre-requisites)
- [How to run on a new codespace](#how-to-run-on-a-new-codespace)
- [User Guide](#user-guide)


## Background Information
The purpose of this project is to highlight the accessibility boundaries within university booking systems and to produce a prototype that can improve awareness so that its functional for all participants. 

To understand the type of issues that impact student participation when navigating these systems, research will be conducted across official documentation, published research and case studies. 

Tools such as WAVE (Web Accessibility Evaluation Tool) (https://wave.webaim.org/) will be used to evaluate disability awareness when operating the booking systems. 

The end goal is to produce a prototype that can improve accessibility for all users and this version of the booking system will aim to meet that goal. 

## Project Features

This booking system provides the following features designed with accessibility in mind:
- **Equipment Inventory**: View current equipment on offer
- **Equipment Browsing**: View equipment organised by category with descriptions and availability status
- **Booking System**: Book a range of equipment 
- **Booking Confirmation**: Receive confirmation details for all equipment bookings
- **Order Management**: View and manage all bookings through an orders page with status tracking
- **Search Equipment**: Type in the name of the equipment to search stock


## Understanding the functionality of WAVE
WAVE is a free browser extension used to measure page accessibility issues on users with disabilities. The extension uses an in-built scoring system called Accessibility IMpact (AIM) which reports on:
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
1. Clone the URL of the project to PyCharm as the chosen IDE.
2. At this current time of documenation, pages are static HTML so open one of the HTML files via the browser support function (Choose the one with the WAVE tool).
3. The page will load and run the WAVE tool.

## Branch information
Use db_v2 when opening a new project as it is the most recent environment.

## Pre-requisites
- Django 6.0
- PyCharm 2025.2.5
- Font Awesome 7.0.0
- Bulma 1.0.3
- WAVE browser extension

## How to run on a new codespace
From the terminal window:

1. Move into the Django app:
	cd mysite
2. Install dependencies:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt
3. Run migrations:
	python manage.py migrate
4. Load fixture data:
	python manage.py loaddata mydata.json
5. Start the server:
	python manage.py runserver 

Notes:
- The fixture file is set up so booking user references are nullable, which avoids foreign key issues on a new database. If it shows user: 1, change to user: null and re-run section 4 onwards. 


## User Guide

### How to Browse and View Equipment Details
1. From the home page, click 'book now'
2. Browse all available equipment displayed within the categories
3. View equipment item


### How to Search Equipment Using the Search Function
1. Navigate to the Equipment page
2. Use the search box at the top of the page
3. Type the name or part of the name of the equipment you're looking for
4. The equipment list will filter to show matching results
5. Results will update as you enter

### How to Make a Booking
1. From the Equipment page, find the item you want to book
2. Click the **Book Now** button on the equipment item
3. When ready, the Booking page is where you need to confirm the order request:
   - Select your start date
   - Select your end date
4. Click **Confirm** to finalise the booking
5. You will receive a confirmation showing the booking details

### How to View Your Orders and Booking History
1. From the homepage, click on **My Orders**
2. You will see a list of all your bookings with the following information:
   - Equipment name
   - Booking dates (start and end date)
   - Current status (Active, Confirmed, or Returned)
   - Date the booking was created

### How to Return an Item
1. Go to **My Orders** page
2. Find the active booking for the item you're returning
3. Click the **Return Item** button
5. The booking status will change to **Returned**
6. Quantity will populate for the equipment to indicate returned item

### How to Change Contrast Themes
1. Look for the **Settings** to select **Themes** in the menu
2. Select your preferred contrast theme from the available options:
   - Normal contrast
   - High contrast
   - Dark mode
3. The theme will apply immediately across all pages
4. Your preference will be saved for future visits