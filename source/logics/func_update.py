def funcDelivery_update(id_client, token_client, list_packages):
    session_id = autentificacion_local(id_client, token_client, "update")

    try:
        response = requests.post(f"{URL_BASEDATA}/search_packages", json={
            "id_session": session_id, 
            "list_packages": list_packages
        }, timeout=10)

        response.raise_for_status()
        data = response.json()

    except requests.exceptions.HTTPError as e:
        if e.response is not None:
           print(f"{' '*4}[!] Error en la peticion")         
        sys.exit(1)

    return data


def main_update(id_client, token_client):
    data = lpm_Userpackage()
    list_packages = []

    print(f"{' '*4}[!] Verificando versiones de los paquetes instalados!\n")

    for name, info in data["package_install"].items():
        list_packages.append(name)

    print(f"{' '*6}[Name Package]{' '*9}[Version]{' '*13}[Lastest]    \n{' '*6}{'-'*20}{' '*3}{'-'*19}{' '*3}{'-'*20}")

    result_packages = funcDelivery_update(id_client, token_client, list_packages)

    print(result_packages)