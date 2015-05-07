#$#
### kein offener Vertrag ohne Austritt:\n";
##foreach ($members_num as $member) {
##   # Keine Vertraege? Wurde oben gemeldet, Naechster!
##   if (!isset($member['vertrag']) || !count($member['vertrag']))
##      continue;
##   # Austritt? Naechster!
##   if (isset($member['Austritt']) && intval($member['Austritt']))
##      continue;
##
##   $vertragoffen = False;
##   foreach ($member['vertrag'] as $vertrag) {
##      if (isset($vertrag['VertragEnde']) && intval($vertrag['VertragEnde']))
##         continue;
##      $vertragoffen = True;
##   }
##
##   if (!$vertragoffen) {
##      if (!isset($warn['vertragnichtoffen']) || !$warn['vertragnichtoffen']) {
##         echo "kein offener Vertrag ohne Austritt:\n";
##         $warn['vertragnichtoffen'] = True;
##      }
##      echo ' '.intval($member['AdrNr']).' "'.$member['Kurzname'].'", '.$member['Nachname'].', '.$member['Vorname']." - Eintritt: ".date("d.m.Y",intval($member['Eintritt']))."\n";
##      foreach ($member['vertrag'] as $vertrag) {
##         echo '   Vertrag: '.$vertrag['ArtName'].' - Beginn: '.date("d.m.Y", intval($vertrag['VertragBegin']))." - Ende: ".date("d.m.Y", intval($vertrag['VertragEnde']))."\n";
##      }
##   }
##}
### * kein offener Vertrag ohne Austritt
##if ($warn['vertragnichtoffen'])
##   echo "\n";
