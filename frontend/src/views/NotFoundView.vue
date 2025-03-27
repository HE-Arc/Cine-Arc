<template>
    <div class="not-found-container">
      <h1>404 - Page non trouvée</h1>
      <p>Oups ! La page que vous recherchez n'existe pas.</p>
      <router-link to="/" class="home-button">Retour à l'accueil</router-link>
    </div>
  </template>
  
  <style scoped>
  .not-found-container {
    text-align: center;
    padding: 50px;
  }
  
  h1 {
    font-size: 2.5rem;
    color: #ff5555;
  }
  
  p {
    font-size: 1.2rem;
  }
  
  .home-button {
    display: inline-block;
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    text-decoration: none;
    border-radius: 5px;
  }
  
  .home-button:hover {
    background-color: #0056b3;
  }
  </style>
  