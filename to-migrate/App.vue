<template>
  <div class="app">
    <header>
      <h1>{{ title }}</h1>
      <nav>
        <ul>
          <li v-for="(item, index) in menuItems" :key="index">{{ item }}</li>
        </ul>
      </nav>
    </header>
    <main>
      <div class="content">
        <h2>{{ subtitle }}</h2>
        <p>{{ message }}</p>
      </div>
      <div class="sidebar">
        <h3>Recent Posts</h3>
        <ul>
          <li v-for="(post, index) in recentPosts" :key="index">{{ post }}</li>
        </ul>
      </div>
    </main>
    <footer>
      <p>&copy; {{ currentYear }} My Vue 3 Website</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      title: 'Complex Vue 3 Website',
      subtitle: 'Explore the Vue ecosystem',
      message: 'Welcome to my website showcasing the features of Vue 3!',
      currentYear: new Date().getFullYear(),
      menuItems: ['Home', 'About', 'Services', 'Portfolio', 'Contact'],
      recentPosts: [
        'Getting Started with Vue 3 Composition API',
        'Building Single Page Applications with Vue Router',
        'State Management with Vuex 4',
      ],
    };
  },
};
</script>

<style>
/* ... your existing styles ... */

nav ul {
  list-style: none;
  padding: 0;
  display: flex;
}

nav li {
  margin-right: 20px;
  cursor: pointer;
  transition: color 0.3s;
}

nav li:hover {
  color: #007bff;
}

.content {
  flex: 2;
}

.sidebar {
  flex: 1;
  background-color: #f7f7f7;
  padding: 20px;
}

/* ... your existing styles ... */
</style>