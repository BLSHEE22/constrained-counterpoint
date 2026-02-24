\version "2.22.4"
\header{
  title = "First Species Counterpoint in G Major"
}

\score {
\new PianoStaff <<
\new Staff { \set Staff.midiInstrument = "harpsichord" \clef "treble" \key  g\major \tempo 4 = 200 g''1 c'''1 b''1 d'''1 c'''1 b''1 c'''1 e'''1 d'''1 fis''1 g''1 }
\new Staff { \set Staff.midiInstrument = "harpsichord" \clef "bass" \key g\major g1 a1 g'1 fis'1 e'1 d'1 e'1 g'1 fis'1 d'1 g1 }
>>
\layout{}
\midi{}
}
