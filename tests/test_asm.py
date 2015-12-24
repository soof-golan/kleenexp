import pytest
from re2.asm import assemble, Literal, Multiple, Either, Concat, CharacterClass, DIGIT, Capture, Setting

def test_literal():
    assert assemble(Literal('abc')) == 'abc'
    assert assemble(Literal('^[a](b)$')) == r'\^\[a\]\(b\)\$'

def test_multiple():
    assert assemble(Multiple(0, 1, True, Literal('a'))) == 'a?'
    assert assemble(Multiple(0, None, True, Literal('a'))) == 'a*'
    assert assemble(Multiple(1, None, True, Literal('a'))) == 'a+'
    assert assemble(Multiple(2, 2, True, Literal('a'))) == 'a{2}'
    assert assemble(Multiple(None, 2, True, Literal('a'))) == 'a{,2}'
    assert assemble(Multiple(2, None, True, Literal('a'))) == 'a{2,}'
    assert assemble(Multiple(2, 5, True, Literal('a'))) == 'a{2,5}'

def test_multiple_subexpression():
    assert assemble(Multiple(0, 1, True, Literal('abc'))) == '(?:abc)?'
    assert assemble(Multiple(0, None, True, Literal('abc'))) == '(?:abc)*'
    assert assemble(Multiple(1, None, True, Literal('abc'))) == '(?:abc)+'
    assert assemble(Multiple(0, 1, True, Multiple(2, 3, True, Literal('a')))) == '(?:a{2,3})?'

def test_multiple_nongreedy():
    assert assemble(Multiple(0, 1, False, Literal('a'))) == 'a??'
    assert assemble(Multiple(0, None, False, Literal('a'))) == 'a*?'
    assert assemble(Multiple(1, None, False, Literal('a'))) == 'a+?'
    assert assemble(Multiple(2, 2, False, Literal('a'))) == 'a{2}?'

def test_either():
    assert assemble(Either(map(Literal, 'abc'))) == 'a|b|c'
    assert assemble(Either(map(Literal, ['123', '45', '']))) == '123|45|'

def test_concat():
    assert assemble(Concat(map(Literal, 'abc'))) == 'abc'
    assert assemble(Concat(map(Literal, ['123', '45', '']))) == '12345'
    assert assemble(Concat([Literal('123'), Multiple(0, 1, True, Literal('abc'))])) == '123(?:abc)?'

def test_character_class():
    assert assemble(DIGIT) == r'\d'
    assert assemble(Concat([DIGIT, DIGIT])) == r'\d\d'
    assert assemble(Concat([DIGIT, Multiple(0, None, True, DIGIT)])) == r'\d\d*'
    assert assemble(CharacterClass(['a'], False)) == r'a'
    assert assemble(CharacterClass(['a', 'b'], False)) == r'[ab]'
    assert assemble(CharacterClass(['a'], inverted=True)) == r'[^a]'
    assert assemble(CharacterClass(['a', 'b'], inverted=True)) == r'[^ab]'

def test_capture():
    assert assemble(Capture(None, DIGIT)) == r'(\d)'
    assert assemble(Concat([Literal('No. '), Capture('number', Multiple(1, None, True, DIGIT))])) == r'No\.\ (?P<number>\d+)'

def test_setting():
    assert assemble(Setting('m', Literal('a'))) == '(?m)a'
    assert assemble(Multiple(0, 1, True, Setting('m', Literal('ab')))) == '(?m)(?:ab)?'
