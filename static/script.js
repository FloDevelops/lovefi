console.log('Hello from script.js')

async function getLinkToken() {
    const path = '/api/create-link-token';
    const response = await fetch(path, { method: 'POST' });

    console.log(response);

    const data = await response.json();
    console.log('data', data);
    if (data) {
        if (data.error != null) {
            console.error('Error creating link token', data.error);
            return;
        }
        console.log('Link token created', data.link_token);
        localStorage.setItem("link_token", data.link_token);
        return data.link_token;
    }
}

async function createPublicToken(linkToken) {
    const handler = Plaid.create({
        token: linkToken,

        //required for OAuth; if not using OAuth, set to null or omit:
        // receivedRedirectUri: window.location.href,

        onSuccess: (public_token, metadata) => {
            console.log('Link success:', public_token);

            fetch('/api/get-access-token', {
                method: 'POST', 
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    public_token: public_token,
                    accounts: metadata.accounts,
                    institution: metadata.institution,
                    link_session_id: metadata.link_session_id,
                }),
            });
        },
        onLoad: () => {
            console.log('Link module loaded.');
        },
        onExit: (err, metadata) => {
            console.error('Link exited with error', err);
        },
        onEvent: (eventName, metadata) => {
            console.log('Link event', eventName, metadata);
        },
        //required for OAuth; if not using OAuth, set to null or omit:
        // receivedRedirectUri: window.location.href,
    });
    handler.open();
}

async function main() {
    let link_token = await getLinkToken();
    if (link_token) createPublicToken(localStorage.getItem("link_token"));
}

main();