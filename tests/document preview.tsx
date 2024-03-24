import React, { useState } from 'react';

const DocumentPreview = () => {
  const [document, setDocument] = useState(null);
  const [showPreview, setShowPreview] = useState(false);
  const [showPrintOptions, setShowPrintOptions] = useState(false);
  const [showShareOptions, setShowShareOptions] = useState(false);
  const [showDownloadConfirmation, setShowDownloadConfirmation] = useState(false);
  const [showShareConfirmation, setShowShareConfirmation] = useState(false);
  const [showPrintConfirmation, setShowPrintConfirmation] = useState(false);

  const handleDocumentClick = () => {
    setShowPreview(true);
  };

  const handlePreviewClose = () => {
    setShowPreview(false);
  };

  const handleDownload = () => {
    // logic to download document
    setShowDownloadConfirmation(true);
  };

  const handleShare = () => {
    setShowShareOptions(true);
  };

  const handleShareOptionSelect = (option) => {
    // logic to share document through selected option
    setShowShareConfirmation(true);
  };

  const handlePrint = () => {
    setShowPrintOptions(true);
  };

  const handlePrintOptionSelect = (option) => {
    // logic to print document with selected options
    setShowPrintConfirmation(true);
  };

  return (
    <div>
      <button onClick={handleDocumentClick}>Click to view document</button>
      {showPreview && (
        <div>
          <button onClick={handlePreviewClose}>Close preview</button>
          <div>{document}</div>
          <button onClick={handleDownload}>Download</button>
          <button onClick={handleShare}>Share</button>
          <button onClick={handlePrint}>Print</button>
        </div>
      )}
      {showDownloadConfirmation && <div>Document downloaded successfully!</div>}
      {showShareOptions && (
        <div>
          <button onClick={() => handleShareOptionSelect('email')}>Email</button>
          <button onClick={() => handleShareOptionSelect('social media')}>Social Media</button>
          <button onClick={() => handleShareOptionSelect('link')}>Link</button>
        </div>
      )}
      {showShareConfirmation && <div>Document shared successfully!</div>}
      {showPrintOptions && (
        <div>
          <button onClick={() => handlePrintOptionSelect('single page')}>Single Page</button>
          <button onClick={() => handlePrintOptionSelect('multiple pages')}>Multiple Pages</button>
          <button onClick={() => handlePrintOptionSelect('specific pages')}>Specific Pages</button>
        </div>
      )}
      {showPrintConfirmation && <div>Document printed successfully!</div>}
    </div>
  );
};
```