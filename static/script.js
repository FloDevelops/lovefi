console.log('Hello from script.js')

async function getLinkToken() {
    const path = '/api/create-link-token';
    const response = await fetch(path, { method: 'POST' });

    // console.log(response);

    const data = await response.json();
    if (data) {
        if (data.error != null) {
            console.error('Error creating link token', data.error);
            return;
        }
        console.log('Link token created', data.link_token);
        localStorage.setItem("link_token", data.link_token);
    }
}

async function getAccessToken(link_token) {
    const path = '/api/set-access-token';
    const response = await fetch(path, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        // body: JSON.stringify({ link_token: link_token }),
    });
    console.log(response);
    console.log('data', await response.json());
}

async function main() {
    await getLinkToken();
    await getAccessToken(localStorage.getItem("link_token"));
}

main