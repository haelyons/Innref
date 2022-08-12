  ## Background
The Wandering Inn is "A tale of a girl, an inn, and a world full of levels." The levels, and classes in which people gain them, are presented with brackets and are 
assigned based on the characters' decisions, path in life, and perspective on themselves -- think DnD, but with less dungeons and more people. Skills, both active and passive are assigned based on Class and are also denoted with square brackets. In addition this story is as of 12/08/22 the longest series in the English language at a whopping 9.3 million words.

As you can imagine, Classes and Skills are not gimmicks, but rather fundamental rules of 'Innworld' which serve as plot and character devices. Pivotal class and skill 
changes most often come at points that are also pivotal for character and plot development. Enter: Innref (or potentially WanderingStat, I'm split).


  ## Goal
I would like to create a web-crawling and natural language processing tool to interpret and provide a reference for readers to rediscover their favorite moments, without 
having to spend an inordinate amount of time re-reading (as enjoyable as this is) or use a Wiki which is frequently out of date (no shade volunteers, it must be difficult) with non-specific chapter references and a general lack of detail.

  ## State of the Tool
I have implemented so far:
- A basic web crawler which parses the table of contents to provide a data-structure with all the chapters, removing repeated chapters
- Parsing all the titles (including Interludes) and sorting all the chapters by date
- Extracting the chapter body from a selected chapter and finding all the bracketed text (class and skill references) and all mentions of levels...

As you may suspect, there is a lot to do....   :)

