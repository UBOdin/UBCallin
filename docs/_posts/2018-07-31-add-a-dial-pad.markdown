---
layout: post
title:  "Use Scratch to Make a Dial Pad"
date:   2018-07-31 18:00:00 -0400
categories: 
  - phone
  - scratch
---

For this project, I'm going to go over how I used scratch to build a dial pad.  You can follow along, and customize the dial pad however you like.  We're also going to learn about scratch lists, loops, and expression blocks.

Normal variables in scratch can each hold one thing at a time.  A list in Scratch is a special type of variable that holds lists of things.  In the Scratch variables palette, click on "Make a list" and name it **digits**.  You'll see a new **digits** list appear at the upper-right corner of the stage, and you'll get a bunch of new blocks.

<center>
  <img src="/images/2018-07-31/MakeAList.png" />
</center>

A phone number in the US is typically ten digits: three digits of area code (e.g., <tt>(716)</tt>) and seven phone number digits (e.g., <tt>123-4567</tt>).  We're going to use the **digits** list to store each of these digits.  The first thing I needed to do was to create sprites to act as dial pad buttons.  I used the 'Choose a new sprite from file' button to add a digit sprite.  The "Letters" folder has sprites for digits and letters in a bunch of different themes.  I used the (futuristic) "Auto" theme and created a sprite that looks like a "1" 

<center>  
  <img src="/images/2018-07-31/NewSpriteFromFile.png" /><br/><br/>
  <img src="/images/2018-07-31/1DigitSprite.png" />
</center>

The script for the sprite had two blocks: 
* *When [Sprite#] is clicked*
* *Add [thing] to [digits]*
I replaced [thing] in the second block with a **1**.  Now, clicking on the "1" sprite adds a new line to the **digits** list with a 1 in it.  I can add as many 1s as I like :).  

<center>  
  <img src="/images/2018-07-31/AddThingToList.png" />
  &nbsp;&nbsp;&nbsp;
  <img src="/images/2018-07-31/ListDisplay.png" />
</center>

Next I added sprites for each of the other nine digits that I could press (remember to replace [thing] with the right digit).  I also needed a way to delete list items.  I chose to create a sprite that looked like a "D" character, but you can use whatever you like.  The script for this sprite looks the same as the digit keys, but instead of a *Add [thing] to [digits]* block, I used a *Delete [1] of [digits]*, and changed **1** to *last* using the pop-up menu.  

<center>  
  <img src="/images/2018-07-31/DeleteThing.png" />
</center>

Next I needed to place a call.  The FONA has no idea how to interpret the **digits** list, so we're going to have to help it by.  I wanted to smush all the digits together into a single **outgoing-number**.  Scratch doesn't have a *Smush* block, so we're going to have to create our own.  Let's think about what it means to smush things together.  We start with the first element, then we add in the second element, then the third, and so forth until we get to the end of the list.  That sounds like a lot of work telling it to smush all of those things together, and computer scientists are lazy... so we're going to find a way to cheat.  We're going to tell scratch how to smush one digit, and then tell it to repeat that instruction a bunch of times.  Let's start by teaching the program how to smush the first two digits together.  To do this, we'll need a new type of block called an Expression block.  These have rounded edges.  I took the sprite I was using to make phone calls, deleted all of the instructions in that sprite's script, and replaced them with:

* *when Sprite# clicked*
* *set [outgoing-number] to [0]*

Now, I didn't want to set outgoing number to 0, I wanted to set it to the first digit of **digits**.  On the Variable palette (Orange), there's an *item [1] of [digits]* block with rounded edges.  I dragged that over the 0, and the the block became part of the *set [outgoing-number] to [...]* block.  

<center>  
  <img src="/images/2018-07-31/Loop-1.png" />
</center>

Clicking on the call button now set **outgoing-number** to whatever the first item of digits is (1 in my case).  Next, I looked at smushing in the second item in the list.  I went to the Operators palette (Green) and dragged a *Join [hello] and [world]* block out into the script area.  Then I went back to the Variables palette (Orange) and dragged the *outgoing-number* block (with rounded edges) over **hello** and *item [1] of [digits]* over **world**, except I replaced the 1 with a 2 (I had to type the 2 in).  Finally I grabbed another *set [outgoing-number] to []* block and dragged the big green/orange/red expression that I'd just created over the 0.  Now, when I click on the dial button, 'outgoing-number' has the first *two* digits ('11' in my case). 

<center>  
  <img src="/images/2018-07-31/Loop-2.png" />
</center>

The next step was to tell Scratch to just repeat the same thing over again.  I grabbed a *Repeat [10]* block from the Control palette (Yellow).  This block looks like a 'C'.  Whatever you put inside the C is what it will repeat 10 times.  I dragged out a *Repeat [10] times* block, dragged the second *set [outgoing-number] to [...]* block into the C, and then dragged the *Repeat [10] times* block to the end of the program.  

<center>  
  <img src="/images/2018-07-31/Loop-3.png" />
</center>

Clicking on the call button now gives me the first digit and ten copies of the second digit... not exactly what I want.  I need a way to pick the second, then third, fourth, fifth, and so forth digits.  The trick to this is something computer scientists call a "loop variable".  I created a new variable using the Make variable button on the Variables palette (Orange) and called it "digit".  Since only this one sprite was going to need it, I created the variable "For this sprite only".  To create a loop variable, we need to add two blocks.  One block to "set the variable up" at the start of the repeat block, and one to update it every time we hit the end of the block.  

1. I added a *Set [digit] to [2]* before the *Repeat [10]* block
2. I added a *Change [digit] by [1]*, which adds 1 to whatever number is in **digit**.  
3. I dragged the *digit* expression block over the 2 in the *Item [2] of [digits]* block.   

<center>  
  <img src="/images/2018-07-31/Loop-4.png" />
</center>

Finally outgoing number is set correctly, so I added a *broadcast [start-call]* block **outside of the repeat "C"** to actually place the call after everything is set. 

<center>  
  <img src="/images/2018-07-31/Loop-5.png" />
</center>

That's it!  Now the scratch program has an actual dial pad so you can call any number!  Try customizing this build yourself.  For example, you might try having the phone show the current number on the screen (e.g., by using costumes in the Looks palette)

<center>  
  <img src="/images/2018-07-31/FinalUI.png" />
</center>
