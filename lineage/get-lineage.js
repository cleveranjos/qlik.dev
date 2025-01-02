(async () => {
    const enigma = require("enigma.js");
    const schema = require("enigma.js/schemas/12.612.0");
    const WebSocket = require("ws");

    // replace with your information
    const appId = "5560bd5f-c520-4ede-bcca-bd24c07bb3fb";
    const tenant = "partner-engineering-saas.us.qlikcloud.com";
    const apiKey = process.env.APIKEY;

    const url = `wss://${tenant}/app/${appId}`;

    const session = enigma.create({
        schema,
        createSocket: () =>
            new WebSocket(url, {
                headers: { Authorization: `Bearer ${apiKey}` },
            }),
    });

    // bind traffic events to log what is sent and received on the socket:
    session.on("traffic:sent", (data) => console.log("sent:", data));
    session.on("traffic:received", (data) => console.log("received:", data));

    // open the socket and eventually receive the QIX global API, and then close
    // the session:
    try {
        const global = await session.open();
        console.log("You are connected!");
        const result = await global.GetActiveDoc({})
        await session.close();
        console.log("Session closed!");
    } catch (err) {
        console.log("Something went wrong :(", err);
    }
})();