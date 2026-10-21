#!/usr/bin/env python3
"""Static regression guards for staged NextGen changes (not a Windows build)."""
from pathlib import Path
root=Path(__file__).resolve().parents[2]
language=(root/'shared/CSystem.cpp').read_text()
enums=(root/'shared/ESystem.h').read_text()
pet=(root/'Server/server/CPetSystemHandler.cpp').read_text()
assert 'GetUserDefaultUILanguage()' in language
assert 'GetUserDefaultLangID()' not in language
assert 'case 0x0416:' in language
assert 'SYSTEMLANGUAGE_PortugueseBrazil' in language and 'SYSTEMLANGUAGE_PortugueseBrazil' in enums
assert 'STORMPK_LANGUAGE' in language
assert 'if (!pcUserData)' in pet
assert 'if (!pcUserData || !pcUserData->pcPetSystem)' in pet
assert 'UPDATE PetSystem SET [PetName] = ? WHERE PetOwnerName=?' in pet
assert '!pcUserData->szAccountName[0] && STRLEN(szNewPetName)' not in pet
# The single-check / insert statement has FOUR parameters; don't break the current binds.
assert 'pcDB->BindParameterInput(4, PARAMTYPE_Integer, &iPetSkin, sizeof(int));' in pet
assert pet.count('VALUES (?,?,?)')==1
print('NEXTGEN_FOUNDATION_STATIC_CHECKS_PASS')
