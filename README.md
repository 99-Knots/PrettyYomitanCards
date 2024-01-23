# PrettyYomitanCards
Trying to provide a visually pleasing and highly functional Anki card format that integrates with the Yomitan browser extension


## How to set up

### Requirements
First, you need to install the necessary programs for the generation of Anki cards:
- [Anki](https://apps.ankiweb.net) flashcard program
- [Yomitan](https://github.com/themoeway/yomitan) browser extension <br/>
  *please note that [Yomichan](https://foosoft.net/posts/sunsetting-the-yomichan-project/) has been discontinued and it is highly recommended for current users to switch to Yomitan instead.
  Instructions for migrating your settings and dictionaries can be found [here](https://github.com/themoeway/yomitan/blob/master/docs/yomichan-migration.md#migrating-from-yomichan).*
- [AnkiConnect](https://ankiweb.net/shared/info/2055492159) AddOn for Anki

- A dictionary for Yomitan <br/>
  Due to big differences in their formating, only some dictionaries may be compatible with this card design. 
  The tested ones include:
   - [Jitendex](https://github.com/stephenmk/Jitendex) - modern format for the J->E JMdict
   - [JMdict](https://github.com/themoeway/jmdict-yomitan#jmdict-for-yomitan-1) - dictionary availabe in various languages
   - [JMnedict](https://github.com/themoeway/jmdict-yomitan#jmnedict-for-yomitan) - readings for different kinds of names and proper nouns
   - [Kanjium](https://github.com/mifunetoshiro/kanjium) - pitch accents *- see [here](https://foosoft.net/projects/yomichan/index.html#dictionaries) for a direct download link*

Instructions for adding dictionaries to Yomitan as well as their download links can be found [here](https://github.com/themoeway/yomitan/blob/master/docs/dictionaries.md).



### Creating the Anki Note Type

In the Anki desktop app, under `Tools > Manage Note Types` click `Add`. You will be prompted to select an existing type as a base. Your choice here doesn't matter as we will be doing quite some customization anyway, so picking `Add:Basic` is fine. Give your new note type a name and click `OK`.

With your new note type selected click on `Fields` and add and delete fields till your card type looks like this:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../main/images/AnkiFieldsDark.png">
  <source media="(prefers-color-scheme: light)" srcset="../main/images/AnkiFields.png">
  <img alt="Screenshot of the Anki note editor showing the fields Expression, Furigana, Pitch, Pitch Graph, Meaning, Sentence, Sentence with furigana, Audio, URL and Notes." src="../main/images/AnkiFields.png" width="518">
</picture>

Pay extra attention to the spelling and capitalization of each field name.
You can ignore the other settings on this page, as they will only affect the appearance of the fields in the card browser.

Save your changes and return to the note types editor, this time selecting `Cards` instead of `Fields`.
Delete all the existing code in the *Front Template* and replace it with the contents of the [frontTemplate.html](../main/frontTemplate.html) file.

Do the same with the *Back Template* using [backTemplate.html](../main/backTemplate.html), and for *Styling* with [style.css](../main/style.css).


### Configuring Yomitan

Open Yomitan's settings page in your browser and navigate to the `Anki` section. 
Make sure your connection with AnkiConnect is enabled and working properly before clicking on `Configure Anki card format...`.

At the top right choose a deck you want your generated cards to be added to and below that on the `Model` field select the new node type you created.
Yomitan will then show you a list of the selected node type's fields. 
Set their values according to the following image:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../main/images/YomitanFieldsDark.png">
  <source media="(prefers-color-scheme: light)" srcset="../main/images/YomitanFields.png">
  <img alt="Screenshot of the Anki card configuration in Yomitan" src="../main/images/YomitanFields.png" width="518">
</picture>

Yomitan will probably fill out most of this automatically but make sure to verify the correct values.
Also note that the *{py-glossary}* entry for the `Meaning` field does not appear in the expandable list. This is normal, you will have to enter it by hand.

Close the popup window when you are done and enable the `Advanced` mode switch at the bottom left of the settings page for the next step.
Without doing so the `Configure Anki card templates...` option will not appear. 
Click it and without changing anything insert the contents of [yomitanTemplate.hbs](../main/yomitanTemplate.hbs) at the bottom of the code window (below the line *{{~> (lookup . "marker") ~}}*).

You can verify this step by typing *{py-glossary}* into the Card Field and pressing `Test`. If it says *"The partial py-glossary could not be found"*, reset the template with the button at the bottom and try again.

You should now be all set up to generate your flashcards from words you find around the web and have them show up in Anki with some nice design and added functionality.
Try clicking the green plus at the top right of the demo in the Yomitan settings to create your first card.


※ To enable Yomitan for local files as well, go to your browser's extension settings page (chrome://extensions when using Chrome for example), find Yomitan there and enable 'allow access to file URLs' for it.


### Stroke Order Popup

To have the popup when hovering over a kanji display their stroke order, you need to install this [Japanese Stroke Order Font](https://www.nihilist.org.uk). 
Instructions for doing so can be found in the [Anki Manual](https://docs.ankiweb.net/templates/styling.html#installing-fonts).


## Further customization

You can easily change the cards' font sizing, which fields should be expanded by default and even the color yourself if you want to.

In Anki open the card editor and search for *var colorRGB*, it should be located at the beginning of the template files.
Within the brackets you can enter the R, G and B values for a new main color of your choosing. 
All other colors in the template and a darker night mode version will be calculated based on those values.
Try for example the combination 120, 150, 100 for a nice sage green.

Below the color you will find variables with a *show_XXX_by_default* naming pattern. Changing those from *false* to *true* will automatically expand the respective field when the card appears in your reviews. 
Slightly further down you will also find variables for the font sizes used on the card. Only enter numbers there, the unit (px) will later be added in the code.

For a consistent appearance those changes will have to be applied both to the front and the back template.


## Other Resources
[Anki-Addon](https://ankiweb.net/shared/info/580654285) for more audio options for Yomichan

Japanese Font selection taken from [here](https://gist.github.com/prantlf/fbd12acc69a022edd589dea48dafe3f8)
