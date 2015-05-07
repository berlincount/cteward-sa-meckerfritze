#$#
### offener Vertrag trotz Austritt:\n";
##foreach ($members_num as $member) {
##   # Keine Vertraege? Wurde oben gemeldet, Naechster!
##   if (!isset($member['vertrag']) || !count($member['vertrag']))
##      continue;
##   # Kein Austritt? Naechster!
##   if (!isset($member['Austritt']) || !intval($member['Austritt']))
##      continue;
##
##   $memberprint = False;
##   foreach ($member['vertrag'] as $vertrag) {
##      if (!isset($vertrag['VertragEnde']) || !intval($vertrag['VertragEnde'])) {
##         if (!isset($warn['vertragoffennachaustritt']) || !$warn['vertragoffennachaustritt']) {
##            echo "offener Vertrag trotz Austritt:\n";
##            $warn['vertragoffennachaustritt'] = True;
##         }
##         if (!$memberprint) {
##            echo ' '.intval($member['AdrNr']).' "'.$member['Kurzname'].'", '.$member['Nachname'].', '.$member['Vorname']." - Austritt: ".date("d.m.Y",intval($member['Austritt']))."\n";
##            $memberprint = True;
##         }
##         echo '   Vertrag: '.$vertrag['ArtName'].' - Beginn: '.date("d.m.Y", intval($vertrag['VertragBegin']))."\n";
##      }
##   }
##}
### * offener Vertrag trotz Austritt
##if ($warn['vertragoffennachaustritt'])
##   echo "\n";
