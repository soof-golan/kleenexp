[![Build Status](https://app.travis-ci.com/SonOfLilit/kleenexp.svg?branch=master)](https://app.travis-ci.com/github/SonOfLilit/kleenexp)

# Kleene Expressions, a modern regular expression syntax

Regular Expressions are one of the best ideas in the programmers ever had. However, Regular Expression _syntax_ is a _^#.\*!_ accident from the late 60s(!), the most horrible legacy syntax for a computer language in common use. It's time to fix it. Kleene Expressions (named after mathematician Stephen Kleene who invented regex) are an easy to learn and use, hard to misuse, drop-in replacement for traditional regular expression syntax. By design, KleenExps **do not** come with their own regex engine - by changing only the syntax and riding on existing regex engines, we can promise full bug-for-bug API compatibility with your existing solution.

Now 100% less painful to migrate! (you heard that right: migration is not painful _at all_)

- [Installation and usage](#installation-and-usage)
- [A Taste of the Syntax](#a-taste-of-the-syntax)
- [How We're Going To Take Over The World](#how-we-re-going-to-take-over-the-world)
  - [Roadmap](#roadmap)
- [Name](#name)
- [Real World Examples](#real-world-examples)
- [Tutorial](#tutorial)
- [Design criteria](#design-criteria)
  - [Migration](#migration)
  - [Syntax](#syntax)
- [Syntax Cheat Sheet](#syntax-cheat-sheet)
- [Grammar (in [parsimonious]() syntax):](#grammar--in--parsimonious----syntax--)
- [License](#license)

# Installation and usage

You can try KleenExp today with Python and/or `grep`, e.g.

```
$ pip install kleenexp
$ echo "Trololo lolo" | grep -P "`ke "[#sl]Tro[0+ [#space | 'lo']]lo[#el]"`"
$ python -c 'import ke; print(ke.search("[1+ #digit]", "Come in no. 51, your time is up").group(0))'
51
```

You can then install the KleenExp VSCode extension from the VSCode extension marketplace and start using it to replace VSCode's Find and Replace dialogue:

!()[Demo animation]

Be sure to read the tutorial below!

# A Taste of the Syntax

The traditional regex:

```
(\d+) Reasons To Switch, The (\d+)th Made Me (?:[Ll][Aa][Uu][Gg][Hh]|[Cc][Rr][Yy])
```

May be written in `ke` as:

```
[#save_num] Reasons To Switch, The [#save_num]th Made Me [case_insensitive ['Laugh' | 'Cry']][#save_num=[capture 1+ #digit]]
```

Or, if you're in a hurry:

```
[c 1+ #d] Reasons To Switch, The [c 1+ #d]th Made Me [ci ['Laugh' | 'Cry']]
```

(and when you're done you can use our automatic tool to convert it to the more readable version and commit that instead.)

More on the syntax, additional examples, and the design criteria that led to its design, below.

# How We're Going To Take Over The World

This is not a toy project meant to prove a technological point. This is a serious attempt to fix something that is broken in the software ecosystem and has been broken since before we were born. We have experience running R&D departments, we understand how technology decisions are made, and we realise success here hinges more on "growth hacking" and on having a painless and risk-free migration story than it does on technical excellence.

**Step 1** would be to introduce KleenExp to the early adopter developer segment by releasing great plugins for popular text editors like Visual Studio Code, with better UX (syntax highlighting, autocompletion, good error messages, ...) and a great tutorial. Adopting a new regex syntax for your text editor is lower-risk, and requires no consultation with other stakeholders.

**Step 2** would be to aim at hobbyist software projects by making our Javascript adoption story as painless and risk-free as possible (since Javascript has the most early-adopting and fast-moving culture). In addition to a runtime drop-in syntax adapter, we will write a `babel` plugin that translates KleenExp syntax into legacy regex syntax at compile time, to enable zero-overhead usage.

**Step 3** would be to aim at startups by optimize and test the implementations until they're ready for deployment in big-league production scenarios

**Step 4** would be to make it possible for large legacy codebases to switch by releasing tools that automatically convert a codebase from legacy syntax to KleenExp (like python's `2to3` or AirBnB's `ts-migrate`)

## Roadmap

- 0.0.1 `pip install`-able, usable in Python projects with `import ke as re` and in `grep` with `` grep -P `ke "pattern"`  ``
- 0.0.2 **We are here** Usable in Visual Studio Code with an extension (requires manually installing the python library)
- 0.0.x Bugfixes and improvements based on community feedback, support 100% of Python and Javascript regex features
- 0.1.0 Usable in Javascript projects, Visual Studio Code extension uses Javascript implementation and does not require any manual installation or configuration
- 0.2.0 Better UX for Visual Studio Code extension through WebView, extensions available for Brainjet IDEs
- 0.3.0 `Babel` plugin enables Javascript projects to use the new syntax with 0 runtime overhead
- 0.9.0 Both implementations are fast, stable and battle tested
- 1.0.0 `2to3`-based tool to automatically migrate Python projects to use new syntax, similar tool for Javascript
- 2.0.0 Implementations for all major languages (Javascript, Python, Java, C#, Go, Kotlin, Scala). Integration into libpcre (or, if we can't get our patches in, stable libpcre fork that keeps in sync with upstream) enables language, editor, database and other tool implementations to effortlessly support KleenExp

# Name

Kleene Expression syntax is named after mathematician Stephen Kleene who invented regular expressions.

Wikipedia says:

> Although his last name is commonly pronounced /ˈkliːni/ KLEE-nee or /kliːn/ KLEEN, Kleene himself pronounced it /ˈkleɪni/ KLAY-nee. His son, Ken Kleene, wrote: "As far as I am aware this pronunciation is incorrect in all known languages. I believe that this novel pronunciation was invented by my father."

However, with apologies to the late Mr. Kleene, "Kleene expressions" is pronounced "Clean expressions" and not "Klein expression".

# Real World Examples

```python
import ke

def remove_parentheses(line):
    if ke.search("([0+ not ')'](", line):
        raise ValueError("Nested parentheses found")
    return ke.sub("([0+ not ')'])", '', line)
assert remove_parentheses('a(b)c(d)e') == 'ace'
```

(the original is from a hackathon project I participated in and looks like this:)

```python
import re

def remove_parentheses(line):
    if re.search(r'\([^)]*\(', line):
        raise ValueError("Nested parentheses found")
    return re.sub(r'\([^)]*\)', '', line)
assert remove_parentheses('a(b)c(d)e') == 'ace'
```

```python
import ke
from django.urls import path, re_path

from . import views

urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    re_path(ke.re('[#start_line]articles/[capture:year 4 #digit]/[#end_line]'), views.year_archive),
    re_path(ke.re('[#start_line]articles/[capture:year 4 #digit]/[capture:month 2 #digit]/[#end_line]'), views.month_archive),
    re_path(ke.re('[#start_line]articles/[capture:year 4 #digit]/[capture:month 2 #digit]/[capture:slug 1+ [#letter | #digit | '_' | '-']]/[#end_line]'), views.article_detail),
]
```

(the original is taken from Django documentation and looks like this:)

```python
from django.urls import path, re_path

from . import views

urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
    re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$', views.article_detail),
]
```

# Tutorial

This is still in Beta, we'd love to get your feedback on the syntax.

Anything outside of brackets is a literal:

```
This is a (short) literal :-)
```

You can use macros like `#digit` (short: `#d`) or `#any` (`#a`):

```
This is a [#lowercase #lc #lc #lc] regex :-)
```

You can repeat with `n`, `n+` or `n-m`:

```
This is a [1+ #lc] regex :-)
```

If you want one of a few options, use `|`:

```
This is a ['Happy' | 'Short' | 'readable'] regex :-)
```

Capture with `[capture <kleenexp>]` (short: `[c <kleenexp>]`):

```
This is a [capture 1+ [#letter | ' ' | ',']] regex :-)
```

Reverse a pattern that matches a single character with `not`:

```
[#start_line [0+ #space] [not ['-' | #digit | #space]] [0+ not #space]]
```

Define your own macros with `#name=[<regex>]`:

```
This is a [#trochee #trochee #trochee] regex :-)[
    [comment 'see xkcd 856']
    #trochee=['Robot' | 'Ninja' | 'Pirate' | 'Doctor' | 'Laser' | 'Monkey']
]
```

Add comments with the `comment` operator (see above.)

Some macros you can use:

| Long Name                                    | Short Name | Definition\*                                                                                                                             | Notes                                                                                                                                                                                                                         |
| -------------------------------------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| #any                                         | #a         | `/./`                                                                                                                                    | May or may not match newlines depending on your engine and whether the kleenexp is compiled in multiline mode, see your regex engine's documentation                                                                          |
| #any_at_all                                  | #aaa       | `[#any \| #newline]`                                                                                                                     |                                                                                                                                                                                                                               |
| #newline_character                           | #nc        | `/[\r\n\u2028\u2029]/`                                                                                                                   | Any of `#cr`, `#lf`, and in unicode a couple more ([explanation](https://stackoverflow.com/questions/1279779/what-is-the-difference-between-r-and-n)]                                                                         |
| #newline                                     | #n         | `[#newline_character \| #crlf]`                                                                                                          | Note that this may match 1 or 2 characters!                                                                                                                                                                                   |
| #not_newline                                 | #nn        | `[not #newline_character]`                                                                                                               | Note that this may only match 1 character, and is _not_ the negation of `#n` but of `#nc`!                                                                                                                                    |
| #linefeed                                    | #lf        | `/\n/`                                                                                                                                   | See also `#n` ([explanation](https://stackoverflow.com/questions/1279779/what-is-the-difference-between-r-and-n)]                                                                                                             |
| #carriage_return                             | #cr        | `/\r/`                                                                                                                                   | See also `#n` ([explanation](https://stackoverflow.com/questions/1279779/what-is-the-difference-between-r-and-n)]                                                                                                             |
| #windows_newline                             | #crlf      | `/\r\n/`                                                                                                                                 | Windows newline ([explanation](https://stackoverflow.com/questions/1279779/what-is-the-difference-between-r-and-n)]                                                                                                           |
| #tab                                         | #t         | `/\t/`                                                                                                                                   |                                                                                                                                                                                                                               |
| #not_tab                                     | #nt        | `[not #tab]`                                                                                                                             |                                                                                                                                                                                                                               |
| #digit                                       | #d         | `/\d/`                                                                                                                                   |                                                                                                                                                                                                                               |
| #not_digit                                   | #nd        | `[not #d]`                                                                                                                               |                                                                                                                                                                                                                               |
| #letter                                      | #l         | `/[A-Za-z]/`                                                                                                                             | When in unicode mode, this will be translated as `\p{L}` in languages that support it (and throw an error elsewhere)                                                                                                          |
| #not_letter                                  | #nl        | `[not #l]`                                                                                                                               |                                                                                                                                                                                                                               |
| #lowercase                                   | #lc        | `/[a-z]/`                                                                                                                                | Unicode: `\p{Ll}`                                                                                                                                                                                                             |
| #not_lowercase                               | #nlc       | `[not #lc]`                                                                                                                              |                                                                                                                                                                                                                               |
| #uppercase                                   | #uc        | `/[A-Z]/`                                                                                                                                | Unicode: `\p{Lu}`                                                                                                                                                                                                             |
| #not_uppercase                               | #nuc       | `[not #uc]`                                                                                                                              |                                                                                                                                                                                                                               |
| #space                                       | #s         | `/\s/`                                                                                                                                   |                                                                                                                                                                                                                               |
| #not_space                                   | #ns        | `[not #space]`                                                                                                                           |                                                                                                                                                                                                                               |
| #token_character                             | #tc        | `[#letter \| #digit \| '_']`                                                                                                             |                                                                                                                                                                                                                               |
| #not_token_character                         | #ntc       | `[not #tc]`                                                                                                                              |                                                                                                                                                                                                                               |
| #token                                       |            | `[#letter \| '_'][0+ #token_character]`                                                                                                  |                                                                                                                                                                                                                               |
| #word_boundary                               | #wb        | `/\b/`                                                                                                                                   |                                                                                                                                                                                                                               |
| #not_word_boundary                           | #nwb       | `[not #wb]`                                                                                                                              |                                                                                                                                                                                                                               |
| #quote                                       | #q         | `'`                                                                                                                                      |                                                                                                                                                                                                                               |
| #double_quote                                | #dq        | `"`                                                                                                                                      |                                                                                                                                                                                                                               |
| #left_brace                                  | #lb        | `[ '[' ]`                                                                                                                                |                                                                                                                                                                                                                               |
| #right_brace                                 | #rb        | `[ ']' ]`                                                                                                                                |                                                                                                                                                                                                                               |
| #start_string                                | #ss        | `/\A/` (this is the same as `#sl` unless the engine is in multiline mode)                                                                |                                                                                                                                                                                                                               |
| #end_string                                  | #es        | `/\Z/` (this is the same as `#el` unless the engine is in multiline mode)                                                                |                                                                                                                                                                                                                               |
| #start_line                                  | #sl        | `/^/` (this is the same as `#ss` unless the engine is in multiline mode)                                                                 |                                                                                                                                                                                                                               |
| #end_line                                    | #el        | `/$/` (this is the same as `#es` unless the engine is in multiline mode)                                                                 |                                                                                                                                                                                                                               |
| #\<char1\>..\<char2\>, e.g. `#a..f`, `#1..9` |            | `[<char1>-<char2>]`                                                                                                                      | `char1` and `char2` must be of the same class (lowercase english, uppercase english, numbers) and `char1` must be strictly below `char2`, otherwise it's an error (e.g. these are errors: `#a..a`, `#e..a`, `#0..f`, `#!..@`) |
| #integer                                     | #int       | `[[0-1 '-'] [1+ #digit]]`                                                                                                                |                                                                                                                                                                                                                               |
| #unsigned_integer                            | #uint      | `[1+ #digit]`                                                                                                                            |                                                                                                                                                                                                                               |
| #real                                        |            | `[#int [0-1 '.' #uint]`                                                                                                                  |                                                                                                                                                                                                                               |
| #float                                       |            | `[[0-1 '-'] [[#uint '.' [0-1 #uint] \| '.' #uint] [0-1 #exponent] \| #int #exponent] #exponent=[['e' \| 'E'] [0-1 ['+' \| '-']] #uint]]` |                                                                                                                                                                                                                               |
| #hex_digit                                   | #hexd      | `[#int [0-1 '.' #uint]]`                                                                                                                 |                                                                                                                                                                                                                               |
| #hex_number                                  | #hexn      | `[1+ #hex_digit]`                                                                                                                        |                                                                                                                                                                                                                               |
| #letters                                     |            | `[1+ #letter]`                                                                                                                           |                                                                                                                                                                                                                               |
| #token                                       |            | `[#letter \| '_'][0+ #token_character]`                                                                                                  |                                                                                                                                                                                                                               |
| #capture_0+\_any                             | #c0        | `[capture 0+ #any]`                                                                                                                      |                                                                                                                                                                                                                               |
| #capture_1+\_any                             | #c1        | `[capture 1+ #any]`                                                                                                                      |                                                                                                                                                                                                                               |
| #vertical_tab                                |            | `/\v/`                                                                                                                                   |                                                                                                                                                                                                                               |
| #bell                                        |            | `/\a/`                                                                                                                                   |                                                                                                                                                                                                                               |
| #backspace                                   |            | `/[\b]/`                                                                                                                                 |                                                                                                                                                                                                                               |
| #formfeed                                    |            | `/\f/`                                                                                                                                   |                                                                                                                                                                                                                               |

\* Definitions `/wrapped in slashes/` are in old regex syntax (because the macro isn't simply a short way to express something you could express otherwise)

```
"[not ['a' | 'b']]" => /[^ab]/
"[#digit | [#a..f]]" => /[0-9a-f]/
```

Trying to compile the empty string raises an error (because this is more often a mistake than not). In the rare case you need it, use `[]`.

Coming soon: `#integer`, `#ip`, ..., `#a..f`, `abc[ignore_case 'de' #lowercase]` (which translates to `abc[['D' | 'd'] ['E'|'e'] [[A-Z] | [a-z]]`, today you just wouldn't try), `[#0..255]` (which translates to `['25' #0..5 | '2' #0..4 #d | '1' #d #d | #1..9 #d | #d]`, `[capture:name ...]`, `[1+:fewest ...]` (for non-greedy repeat), unicode support. Full PCRE feature support (lookahead/lookback, some other stuff). See TODO.txt.

# Design criteria

## Migration

Ease of migration trumps any other design consideration. Without a clear, painless migration path, there will be no adoption.

- Capabilities should be exactly equivalent to those of legacy regex syntax
- Provide a tool to translate between legacy and kleenexp syntax to aid in learning and porting existing code
- Provide a tool to translate between short and long macro names (because typing `[#start_line [1+ #letter] #end_line]` instead of `^[a-zA-Z]+$`
- Provide plugins for popular IDEs (vscode, IntelliJ, ...) that wrap existing find/replace functionality with kleenexp support, with good syntax highlighting and macro name autocomplete
- Provide libraries for every common language with a function to convert kleenexp syntax to the language's legacy native syntax, and a factory that constructs compiled regex objects (since it returns a native regex engine object, no code changes will ever be required except for translating the patterns)
- Provide a command line tool, e.g. `` $ grep "`ke "[1+ #d] Reasons"`" ``

## Syntax

- Should be easy to read
- Should be easy to teach
- Should be easy to type (e.g. "between 3 and 5 times" is not a very good syntax)
- Should minimize comic book cursing like ^[^#]\*$
- Should make simple expressions literals (i.e. /Yo, dawg!/ matches "Yo, dawg!" and no other string)
- Should only have 1-2 "special characters" that make an expression be more than a simple literal
- Should not rely on characters that need to be escaped in many use cases, e.g. `"` and `\` in most languages' string literals, `` ` `` `$` in bash (`'` is OK because every language that allows `'` strings also allows `"` strings. Except for SQL. Sorry, SQL.)
- Different things should look different, beware of Lisp-like parentheses forests
- Macros (e.g. a way to write the [IP address regex](https://regex101.com/r/oE7iZ2/1) as something like `/\bX.X.X.X\b where X is (?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)/`

# Syntax Cheat Sheet

```
This is a literal. Anything outside of brackets is a literal (even text in parentethes and 'quoted' text)
Brackets may contain whitespace-separated #macros: [#macro #macro #macro]
Brackets may contain literals: ['I am a literal' "I am also a literal"]
Brackets may contain pipes to mean "one of these": [#letter | '_'][#digit | #letter | '_'][#digit | #letter | '_']
If they don't, they may begin with an operator: [0-1 #digit][not 'X'][capture #digit #digit #digit]
This is not a legal kleenexp: [#digit capture #digit] because the operator is not at the beginning
This is not a legal kleenexp: [capture #digit | #letter] because it has both an operator and a pipe
Brackets may contain brackets: [[#letter | '_'] [1+ [#digit | #letter | '_']]]
This is a special macro that matches either "c", "d", "e", or "f": [#c..f]
You can define your own macros: ['#' [[6 #h] | [3 #h]] #h=[#digit | #a..f]]
There is a "comment" operator: ['(' [3 #d] ')' [0-1 #s] [3 #d] '.' [4 #d] [comment "ignore extensions for now" [0-1 '#' [1-4 #d]]]]
```

# Grammar (in [parsimonious](https://github.com/erikrose/parsimonious) syntax):

```
regex           = ( outer_literal / braces )*
braces          = '[' whitespace? ( ops_matches / either / matches )? whitespace? ']'
ops_matches     = op ( whitespace op )* ( whitespace matches )?
op              = token (':' token)?
either          = matches ( whitespace? '|' whitespace? matches )+
matches         = match ( whitespace match )*
match           = inner_literal / def / macro / braces
macro           = '#' ( range_macro / token )
range_macro     = range_endpoint '..' range_endpoint
def             = macro '=' braces

outer_literal   = ~r'[^\[\]]+'
inner_literal   = ( '\'' until_quote '\'' ) / ( '"' until_doublequote '"' )
until_quote     = ~r"[^']*"
until_doublequote = ~r'[^"]*'

# if separating between something and a brace, whitespace can be optional without introducing ambiguity
whitespace      = ~r'[ \t\r\n]+|(?<=\])|(?=\[)'
# '=' and ':' have syntactic meaning
token           = ~r'[A-Za-z0-9!$%&()*+,./;<>?@\\^_`{}~-]+'
range_endpoint  = ~r'[A-Za-z0-9]'
```

# License

`ke` is distrubuted under the MIT license:

```
Copyright (c) 2015-2021, Aur Saraf

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
