export async function fetchJSON(url, options = {}) {
    const headers = {Accept: 'application/json', ...options.headers};
    const response = await fetch(url, {...options, headers});

    if (response.ok) {
        return response.json();
    }
    throw new Error('Erreur serveur', {cause: response});
}