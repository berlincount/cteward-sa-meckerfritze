#$#
##
### Alter < ~18
##foreach ($members_num as $member) {
##   if ($member['Alter'] && $member['Alter'] < ~18) {
##      if (!isset($warn['mindestalter']) || !$warn['mindestalter']) {
##         echo "Alter < ~18:\n";
##         $warn['mindestalter'] = True;
##      }
##      echo ' '.intval($member['AdrNr']).' "'.$member['Kurzname'].'", '.$member['Nachname'].', '.$member['Vorname']." - ".$member['Geburtsdatum']." (~".$member['Alter'].")\n";
##   }
##}
### * Alter < ~18
##if ($warn['mindestalter'])
##   echo "\n";
##
