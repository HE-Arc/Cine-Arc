<template>
  <div class="about container">
    <!-- Main heading for the About page -->
    <h1>À propos de Ciné-Arc</h1>
    <hr class="w-25 mx-auto">
    <!-- Introduction paragraph for the platform -->
    <p style="text-align: center;">Bienvenue sur <strong>Ciné-Arc</strong>, votre plateforme dédiée à la réservation de séances de cinéma en ligne !</p>

    <section>
      <!-- Subheading for the first section -->
      <h2>Votre cinéma, à portée de clic</h2>
      <!-- Description of the platform's purpose and user experience -->
      <p>
        Ciné-Arc vous permet de consulter facilement les films à l’affiche, de vérifier les horaires des séances et de réserver vos places en toute simplicité.
        Grâce à une interface intuitive, profitez d’une expérience fluide et agréable.
      </p>
    </section>

    <section>
      <!-- Subheading for the features section -->
      <h2>Fonctionnalités principales</h2>
      <!-- List of main features offered by the platform -->
      <ul>
        <li>Accédez aux films actuellement à l'affiche avec des informations détaillées.</li>
        <li>Réservez vos séances dans l'une de nos trois salles de cinéma.</li>
        <li>Paiement sécurisé via Stripe.</li>
        <li>Gérez vos réservations et consultez vos billets.</li>
      </ul>
    </section>

    <section>
      <!-- Subheading for the team section -->
      <h2>Notre équipe</h2>
      <!-- List of team members -->
      <ul>
        <li>Marilyn Teuscher</li>
        <li>Bryan Dos Santos</li>
        <li>Simon Berthoud</li>
        <li>Julien Annen</li>
      </ul>
    </section>

    <footer>
      <!-- Footer with copyright information -->
      <p>© 2024 Ciné-Arc. Tous droits réservés.</p>
    </footer>
  </div>
</template>

<style>
/* Styling for the container to center content and set max width */
.container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  text-align: left;
}

/* Styling for the main heading */
h1 {
  text-align: center;
  color: #d35400;
}

/* Styling for subheadings */
h2 {
  margin-top: 30px;
  color: #555;
  font-size: 1.2em;
}

/* Styling for unordered lists */
ul {
  list-style-type: disc;
  margin-left: 20px;
}

/* Styling for the footer */
footer {
  margin-top: 40px;
  text-align: center;
  font-size: 0.9em;
  color: #777;
}
</style>
