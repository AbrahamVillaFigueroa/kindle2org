# kindle2org
## Description
kindle2org is a  Python program that takes the notes, highlights and bookmarks stored in an Amazon Kindle and transforms them into an Org document that is more organized and that is easier to work with.

The program uses as input a standard "My Clippings.txt" file from the Amazon Kindle. Then it produces an Org Mode file with all its contents organized.

## How to use

To use it, write in the terminal:

~~~
$ python kindle2org.py <MYCLIPPINGS.txt> <ORGFILE.org>
~~~

For example:
~~~
$ python kindle2org.py "My Clippings.txt" my-clippings.org
~~~

## Structure of the output file

In the output Org file, a header will be created with a title and a date of import.

There will be as many headings as books are quoted in your clippings file.

Under the title of the book, there will be up to three subheadings: notes, highlights and bookmarks.

**Notes.** Here are included all your written notes. The text of each subheading is the text you wrote on your kindle. kindle2org will identify the quote associated with this note and it will write it underneath. The location and the page of the quote are also included.

**Highlights.** Here are included all your highlights of the current book that don't have a note associated to them. If they do, they can only be found under the **Notes** subheading. They are organized by date and they include at the end of the quote the location and the page where they come from.

**Bookmarks.** These are included as a list of pages and locations. They have no quote associated to it. The date and time when the bookmark was made is also included in each entry.

As an example, the resulting Org text from one book will look like this:

~~~
* How to Listen to Jazz | Ted Giogia
** Notes
*** Structure of short jazz songs
#+begin_quote
But when a song is fairly short, say twelve or sixteen bars in duration, the musicians typically play the melody twice at the beginning and conclusion of the performance. These three options—thirty-two-bar songs, twelve-bar songs, sixteen-bar songs—account for the vast majority of the jazz performed since the early 1930s.
—Location 661-663, page 44
#+end_quote
** Highlights
*** Made on Sunday, February 7, 2021 5:48:48 PM
#+begin_quote
The most common thirty-two-bar song form in American twentieth-century popular music and jazz is AABA.
—Location 685-685, page 45
#+end_quote
** Bookmarks
- Location 19, page 2, made on Sunday, June 28, 2020 9:06:46 PM
- Location 19, page 2, made on Sunday, June 28, 2020 9:07:00 PM
~~~

## Important note
"My Clippings.txt" file must have the standard format for this script to work properly. 

## Trick for Org Tags 
Beacuse the text of the Kindle's annotations is transformed into an Org heading, you can write at the end of your note tags in Org format that will be propery formatted. So for example, if you write ":music:jazz:criticism:" at the end of an annotation, kindle2org will properly put it at the end of a subheading in the Org document. This can be useful for organizing your highlights in a more precise manner.

