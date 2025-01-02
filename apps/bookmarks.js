import { auth, qix } from '@qlik/api';

const appId = "5ab9e279-db6f-4561-bc81-f3afd7583ba3";

(async () => {
    auth.setDefaultHostConfig({
        authType: "oauth2",
        host: "partner-engineering-saas.us.qlikcloud.com",
        clientId: "c8492b4ae2130d9dbca68dbdb7a37ae0",
        clientSecret: "ba81a905d2e6772d3318e1043fb336416f8103025e7e19a149fc15c104b4c15d",
        scope: "user_default admin.apps admin_classic",
    });

    const app = await qix.openAppSession(appId).getDoc();
    const bookmarks = await app.getBookmarks({
        qOptions: {
            qTypes: ["bookmark"]
        },
    });
    let i = 0;
    for (let bookmark of bookmarks) {
        let qMeta = bookmark.qMeta
        console.log(++i, qMeta.title, qMeta.owner, qMeta.approved, qMeta.published);
    }
    process.exit();
})();