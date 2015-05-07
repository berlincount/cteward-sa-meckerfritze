### Unbefristeter Sozialtarif fuer nicht-(Alters-)Rentner (<~65)
##foreach ($members_num as $member) {
##   if (!isset($member['vertrag']) || !count($member['vertrag']))
##      continue;
##   foreach ($member['vertrag'] as $vertrag) {
##      if ($vertrag['Art'] == 3 && !$vertrag['VertragEnde'] && $member['Alter'] < 65) {
##         if (!isset($warn['vertragsozialfrist']) || !$warn['vertragsozialfrist']) {
##            echo "Unbefristeter Sozialtarif fuer nicht-(Alters-)Rentner (<~65):\n";
##            $warn['vertragsozialfrist'] = True;
##         }
##         echo ' '.intval($member['AdrNr']).' "'.$member['Kurzname'].'", '.$member['Nachname'].', '.$member['Vorname']." - ".$member['Geburtsdatum']." (~".$member['Alter'].")\n";
##      }
##   }
##}
### * Unbefristeter Sozialtarif fuer nicht-(Alters-)Rentner (<~65)
##if ($warn['vertragsozialfrist'])
##   echo "\n";
