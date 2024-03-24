import React, { useState, useEffect } from 'react';

const MobileResponsiveDesign = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isFormSubmitted, setIsFormSubmitted] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 768) {
        setIsMobile(true);
      } else {
        setIsMobile(false);
      }
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  const handleMenuClick = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const handleFormSubmit = () => {
    setIsFormSubmitted(true);
  };

  return (
    <div>
      <h1>Mobile Responsive Design</h1>
      <p>
        Given I am on the website
        {isMobile && <span> on a mobile device</span>}
      </p>
      <p>
        When I view the website
        {isMobile && <span> on a mobile device</span>}
      </p>
      <p>
        Then the website should be responsive and adjust to fit the screen size
      </p>
      <button onClick={handleMenuClick}>Navigation Menu</button>
      {isMenuOpen && (
        <div>
          <p>Option 1</p>
          <p>Option 2</p>
          <p>Option 3</p>
        </div>
      )}
      <p>
        Given I am on the website
        {isMobile && <span> on a mobile device</span>}
      </p>
      <p>
        When I click on the navigation menu
        {isMobile && <span> on a mobile device</span>}
      </p>
      <p>Then the menu should expand and display all options</p>
      <p>
        Given I am on the website
        {isMobile && <span> on a mobile device</span>}
      </p>
      <p>
        When I scroll through the website
        {isMobile && <span> on a mobile device</span>}
      </p>
      <p>Then the content should adjust and be easy to read and navigate</p>
      <form onSubmit={handleFormSubmit}>
        <label htmlFor="name">Name:</label>
        <input type="text" id="name" />
        <label htmlFor="email">Email:</label>
        <input type="email" id="email" />
        <label htmlFor="message">Message:</label>
        <textarea id="message" />
        <button type="submit">Submit</button>
      </form>
      {isFormSubmitted && <p>Form submitted successfully!</p>}
      <p>
        Given I am on the website
        {isMobile && <span> on a mobile device</span>}
      </p>
      <p>
        When I fill out the form
        {isMobile && <span> on a mobile device</span>}
      </p>
      <p>Then the form should be easy to use and submit on a mobile device</p>
    </div>
  );
};

export default MobileResponsiveDesign;