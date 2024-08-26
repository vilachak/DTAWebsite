# Copyright 2022-2023, IT Cell, Directorate of Treasuries & Accounts, Nagaland. All rights reserved.
import enum


class UserTypeEnum(str, enum.Enum):
    ADMIN = 'ADMIN'
    DISTRICT = 'DISTRICT'


LOGIN_REDIRECT = {
        UserTypeEnum.ADMIN: 'dashboard',
        UserTypeEnum.DISTRICT: 'dashboard',
    }
