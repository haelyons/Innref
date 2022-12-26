  ## Background
The Wandering Inn is "A tale of a girl, an inn, and a world full of levels." The levels and classes in which people gain them are presented in the text with square brackets [], and are 
assigned based on the characters' decisions, path in life, and perspective on themselves -- think DnD, but without NPCs! Active and passive Skills are assigned based on Class and are also denoted with square brackets. 

As you can imagine, Classes and Skills are not gimmicks, but rather fundamental rules of 'Innworld' which serve as plot and character devices. Pivotal class and skill changes most often come at points that are also pivotal for character and plot development. 

The idea for this tool comes from a combination of these markers, and the current length of the serial - 9.3 million words. Using the easy references provided by Skills and Classes, we can pinpoint the moments we want for key-rereads, and provide up-to-date info for Wiki editors.

  ## Goal
I would like to create a web-crawling and natural language processing tool to provide a reference for readers to find their favorite moments, as well as for Wiki maintainers to have an easier time finding relevant chapter content. The main element I would like to track are individuals within their story -- a clear list of their Class and related Skills with chapter references for each mention of their Class, Level or Skill.

  ## State
I have implemented so far:
- A basic web crawler which parses the table of contents to provide a data-structure with all the chapters, removing repeated chapters
- Parsing all the titles (including Interludes) and sorting all the chapters into a neat TOC
- Extracting the chapter body from a selected chapter URL and finding all the bracketed text (class and skill references) and all mentions of levels


As you may suspect, there is a lot to do...   :)

