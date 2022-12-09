# AppexOppgave
""
Lag en web applikasjon som lar deg lagre potensielle kunder basert på oppslag/data om bedrifter fra Brønnøysundregisteret. 
Brukeren må kunne registrere/lagre ekstra informasjon om hver bedrift, f.eks. et notat.
 
Hent inn/vis data fra ett eller flere andre API’er basert på org.nr./postnr. koblet til bedriften. Forskjellige åpne API’er kan du finne her: https://data.norge.no/.

""
__________________________________________________________________________________________________________________________________________

Dette programmet bruker: https://data.brreg.no/enhetsregisteret/oppslag/enheter/lastned/regneark excel arket, som du må lagre som .csv fil.

Når du åpner programmet trykker du på "Åpne fil" knappen og velger .csv filen ("enheter_alle") 

Etter det kan du søke på en næringskode beskrivelse og programmet vil gi lignende resultater basert på input i søkefeltet.

Når du trykker "Søk" så søker den etter næringskode og gir deg en liste med bedrifter.

du kan trykke på hvilken som helst bedrift i tabellen og deretter trykke "Velg" og så blir alt informasjonen fra .csv filen om den bedriften hentet ut
og lagt inn i tekstvinduet oppe til høyre.

over tekstvinduet fins det to linker som tar deg til bedriftens nettside, og bruker organisasjonsnummeret som tar deg til proff.no

under så kan du skrive notater og lagre de i en tekstfil, der infoen fra tabellen og notatene dine blir lagret sammen.
