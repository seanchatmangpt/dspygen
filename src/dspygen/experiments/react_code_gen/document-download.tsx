import React, { useState, useEffect } from 'react';

const DocumentDownload = () => {
  const [downloaded, setDownloaded] = useState(false);

  useEffect(() => {
    if (downloaded) {
      // download document
    }
  }, [downloaded]);

  return (
    <div>
      <button onClick={() => setDownloaded(true)}>Download</button>
    </div>
  );
};
```