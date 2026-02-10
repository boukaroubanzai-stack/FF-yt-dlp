browser.contextMenus.create({
  id: "ytdlp-download",
  title: "Download with yt-dlp",
  contexts: ["video", "page", "link"]
});

browser.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId !== "ytdlp-download") return;

  const url = info.linkUrl || info.pageUrl || tab.url;

  browser.runtime.sendNativeMessage("ff_ytdl", { url })
    .then(response => {
      if (response.status === "ok") {
        console.log("yt-dlp launched for:", url);
      } else {
        console.error("yt-dlp error:", response.message);
      }
    })
    .catch(error => {
      console.error("Native messaging error:", error);
    });
});
