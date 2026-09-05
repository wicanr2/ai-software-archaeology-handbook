'use strict';
const share = document.querySelector('#share');
const status = document.querySelector('#share-status');
if (share && navigator.clipboard && window.isSecureContext) {
  share.hidden = false;
  share.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText('https://wicanr2.github.io/ai-software-archaeology-handbook/');
      status.textContent = '網站連結已複製。';
    } catch {
      status.textContent = '無法自動複製，請複製瀏覽器網址列的連結。';
    }
  });
}
