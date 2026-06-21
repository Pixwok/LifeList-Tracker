export async function fetchJSON(url, options = {}) {
    const header = {Accept: 'application/json', ...options.header};
    const response = await fetch(url, {...options, header});

    if (response.ok) {
        return response.json();
    }
    throw new Error('Erreur serveur', {cause: response});
}