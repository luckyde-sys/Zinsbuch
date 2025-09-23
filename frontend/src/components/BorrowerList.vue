<template>
  <div>
    <h2>Borrowers</h2>
    <ul>
      <li v-for="borrower in borrowers" :key="borrower.id">
        {{ borrower.name }} - {{ borrower.phone }} - {{ borrower.email }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      borrowers: []
    }
  },
  mounted() {
    const backendUrl = 'http://localhost:5000'  // Your Flask backend URL
    fetch(`${backendUrl}/borrowers`)
      .then(response => response.json())
      .then(data => {
        this.borrowers = data
      })
      .catch(err => console.error('Error fetching borrowers:', err))
  }
}
</script>
