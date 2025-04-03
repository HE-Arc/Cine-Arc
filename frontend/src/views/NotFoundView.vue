<template>
  <!-- Main container for the 404 Not Found page -->
  <div class="not-found-container">
    <!-- Heading for the 404 error -->
    <h1>404 - Page non trouvée</h1>
    <!-- Message to inform the user that the page does not exist -->
    <p>Oups ! La page que vous recherchez n'existe pas.</p>
    <!-- Link to redirect the user back to the homepage -->
    <router-link to="/" class="home-button">Retour à l'accueil</router-link>
  </div>
</template>

<style scoped>
  /* Styling for the main container */
  .not-found-container {
  text-align: center; /* Center align text */
  padding: 50px; /* Add padding around the container */
  }

  /* Styling for the heading */
  h1 {
  font-size: 2.5rem; /* Set font size */
  color: #ff5555; /* Set text color to red */
  }

  /* Styling for the paragraph */
  p {
  font-size: 1.2rem; /* Set font size */
  }

  /* Styling for the home button */
  .home-button {
  display: inline-block; /* Display as an inline block */
  margin-top: 20px; /* Add margin above the button */
  padding: 10px 20px; /* Add padding inside the button */
  background-color: #007bff; /* Set background color to blue */
  color: white; /* Set text color to white */
  text-decoration: none; /* Remove underline from the link */
  border-radius: 5px; /* Add rounded corners */
  }

  /* Styling for the home button on hover */
  .home-button:hover {
  background-color: #0056b3; /* Change background color on hover */
  }
</style>
