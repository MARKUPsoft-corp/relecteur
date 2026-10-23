def est_majeur(age):
    """Vérifie si une personne est majeure (>= 18 ans)."""
    if not isinstance(age, (int, float)):
        raise TypeError("L'âge doit être un nombre")
    return age >= 18
