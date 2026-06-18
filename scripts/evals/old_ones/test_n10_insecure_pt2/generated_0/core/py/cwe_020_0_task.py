def get_target_for_redirect(target: str, domain: str) -> str:
    if target.startswith('https://' + domain):
        return target
    else:
        return 'https://' + domain