<template>
    <v-footer>
      <v-container class="footer">
        <v-row>
          <!-- First Column -->
          <v-col cols="12" md="3" class="footer-column">
            <v-img
              src="@/assets/images/skagen-icon.png"
              max-width="38"
              max-height="38"
              class="mb-3"
              alt="Skågen Logo"
            ></v-img>
            <p class="small-gray">Ideas that ripple</p>
            <v-divider class="my-3"></v-divider>
            <div class="social-icons">
              <v-btn variant="flat" icon size="x-small" class="social-btn" href="https://linkedin.com" target="_blank">
                <v-icon>mdi-linkedin</v-icon>
              </v-btn>
              <v-btn variant="flat" icon size="x-small" class="social-btn" href="https://mastodon.social" target="_blank">
                <v-icon>mdi-elephant</v-icon>
              </v-btn>
              <v-btn variant="flat" icon size="x-small" class="social-btn" href="https://bsky.app" target="_blank">
                <v-icon>mdi-twitter</v-icon>
              </v-btn>
            </div>
          </v-col>
  
          <!-- Second Column -->
          <v-col cols="12" md="3" class="footer-column">
            <h5 class="footer-title">Developers</h5>
            <ul class="footer-list">
              <li>API automation</li>
              <li>Github</li>
              <li>ActivityPub</li>
              <li>Solid wallets</li>
            </ul>
          </v-col>
  
          <!-- Third Column -->
          <v-col cols="12" md="3" class="footer-column">
            <h5 class="footer-title">Company</h5>
            <ul class="footer-list">
              <li>About</li>
              <li>Contact</li>
              <li>Join us</li>
              <li>Press</li>
            </ul>
          </v-col>
  
          <!-- Fourth Column -->
          <v-col cols="12" md="3" class="footer-column">
            <h5 class="footer-title">Get the latest news and updates</h5>
            <p class="smaller-text mb-4">
              Join our community to receive updates about our latest advancements.
            </p>
            <form class="email-form">
              <div class="custom-input">
                <input type="email" placeholder="Enter your email" />
              </div>
              <button class="custom-button" type="submit">Subscribe</button>
            </form>
          </v-col>
        </v-row>
  
        <v-divider class="my-4"></v-divider>
  
        <!-- Second Row -->
        <v-row align="center" justify="space-between">
          <v-col cols="12" md="6" class="copyright">
            <p>Copyright © 2024 Skågen. All rights reserved.</p>
          </v-col>
          <v-col cols="12" md="6" class="footer-links" align="end">
            <a href="/terms" class="footer-link smaller-gray">Terms & Conditions</a>
            <span>|</span>
            <a href="/privacy" class="footer-link smaller-gray">Privacy Policy</a>
            <span>|</span>
            <span class="smaller-gray px-2">Language:</span> 
            <div class="custom-dropdown">
              <select class="smaller-gray">
                <option value="en">English</option>
                <option value="fr">French</option>
                <option value="nl">Dutch</option>
              </select>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-footer>
  </template>
  
  <script>
  export default {
    name: "AppFooter",
  };
  </script>
  
  <style scoped>
  .footer {
    color: var(--clr-subtext);
  }
  
  .footer-column {
    margin-bottom: 16px;
  }
  
  .footer-title {
    font-weight: bold;
    margin-bottom: 8px;
  }
  
  .gray-text {
    color: gray;
    margin: 8px 0;
  }
  
  .social-icons .social-btn {
    margin-right: 8px;
    color: #555;
  }
  
  .email-form {
    display: flex;
    align-items: center;
  }
  
  .custom-input {
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 6px 8px;
    margin-right: 8px;
    flex: 1;
  }
  
  .custom-input input {
    border: none;
    outline: none;
    width: 100%;
    font-size: 0.875rem;
  }
  
  .custom-button {
    background-color: #665bda;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 0.875rem;
    cursor: pointer;
  }
  
  .custom-button:hover {
    background-color: #584fc4;
  }
  
  .footer-links {
    text-align: right;
  }
  
  .footer-link {
    margin: 0 8px;
    text-decoration: none;
  }
  
.smaller-gray {
    font-size: 0.75rem;
    color: gray;
  }
  
  .footer-link:hover {
    text-decoration: underline;
  }
  
  .custom-dropdown {
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 4px;
  }
  
  .custom-dropdown select {
    border: none;
    outline: none;
    background: none;
    font-size: 0.75rem;
    color: gray;
    cursor: pointer;
  }
  
  .smaller-text {
    font-size: 0.875rem;
  }
  
  .footer-list {
    list-style-type: none;
    padding-left: 0;
  }
  
  .footer-list li {
    font-size: 0.875rem;
  }
  
  .copyright {
    color: gray;
    font-size: 0.75rem;
  }
  </style>
  