"""
Module authentification et rôles — Aurélien (LaNuggets)

Couvre : US-17 (contrôle d'accès), US-18 (rôles admin/user).

⚠️ Hotfix : ce fichier re-exporte les fonctions réellement implémentées dans
`access_control.py` (US-17) et `roles.py` (US-18) pour que `app.py` puisse les
utiliser via `from modules import auth`.
"""
from __future__ import annotations

from modules.access_control import (  # noqa: F401
    authenticate,
    hash_password,
    load_users,
    login_form,
    logout,
    require_auth,
)
from modules.roles import (  # noqa: F401
    PERMISSIONS,
    ROLES,
    has_permission,
    require_role,
)
