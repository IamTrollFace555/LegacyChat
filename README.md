# LegacyChat
An AI-Powered Chat Service to Preserve Family Wisdom

# Bootstrap elements to check out
- Cards
- Alerts
- Carousel

# Writing levels
- Bachelor
- No formal education
- Experienced writer
- Casual Writer
- School Kid

# TO DO's

- [IMPORTANT] When we are finished with a section we should have a page (where question 21 would be). It should say “ congratulations you have answered the questions to help us create your persona”. Here are the questions and answers below.
- Download your summary/chapters
- [IMPORTANT] Free trial with fewer questions (Maybe 5?)
- [IMPORTANT] Add the option to generate multiple versions(passes) of the chapter (up to 4)
- See what changed between the questions and the model output
- Add Email Verification
- Add Google authentication
- Delete chapters
- [ABORTED] Return to subchapter selection from "/questionnaire"
- [IMPORTANT] Save the API key as an environment variable

# Recently Done

- Fix the prompt for chapter0 (Author Foreword)
- Answers are now automatically saved every two minutes. A status bar signals the last time answers were saved
- A "skip question" button
- Defined subchapters for ch1 and ch2
- Now you can choose a subchapter to answer a smaller set of questions instead of the whole 20 questions of the questionnaire

# Done

- When completed chapter0: let’s test out your persona: “Write a one-page letter that I can email to a son or daughter having a challenge time sharing how I have dealt a hard challenge”
- Update Dashboard (Javier's email) ([LATER] fixed the dashboard)
- Updated the GUI style
- "See password" button
- Add a button to log out
- Email already exists (register)
- Incorrect email or password (login)
- Password recovery
- Each page should have its own title
- Change font size
- For Questionnaires: Submit (Save) shouldn’t take you back to the home page, Just save and say “saved” when done.
- Add a home button to get back to the main page to the right of the next button (questionnaire) (Implemented as the "Save and exit" button")





# Meeting with larry

Time:  Product within two months

- Something that works rather well
- Flow 
  - Dashboard is now the control panel
  - Photos (not included in the MVP) Sub-chapters for photos
  - Table of answers
  
1. Go to the control table

- [Important] Get products in the hands of testers
- Save questions when hitting "next" or "previous"
- New column for "summary" of the chapter
- Buttons to change the prompt (Customize prompt)

- [IMPORTANT] Retry generating a chapter
- Retry as many times as you like and save all tries. (4 tries for the first version)

Things that you should be able to change:
- Writing level (Uni, Schooler)
- Tone (Friendly, Bussines like, etc, ...)
- Change temperature of the model (Creativity)
- Select the try that you want for the final document

- Final file should be downloadable.