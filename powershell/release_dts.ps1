$VersionNumber = 12
$RevisionNumber = 1
$ReleaseNumber = 2403
$PatchNumber = 10

$hash = "{0:X8}{1:X8}{2:X8}{3:X8}" -f $VersionNumber, $RevisionNumber, $ReleaseNumber, $PatchNumber

printf("$hash\n")
