<script>
//import { driver, auth } from 'neo4j-driver'
import * as neo4j from "neo4j-driver";
//import * as neo4jDriver from "neo4j-driver";

//const neo4j = require('neo4j-driver')



// try {
//   const result = await session.run(
//       'CREATE (a:Person {name: $name}) RETURN a',
//       { name: personName }
//   )
//
//   const singleRecord = result.records[0]
//   const node = singleRecord.get(0)
//
//   console.log(node.properties.name)
// } finally {
//   await session.close()
// }

// on application exit:

// await driver.close()

export default {
  methods: {
    handleClick() {
      console.log("in func handleClick");
      const uri = "neo4j://localhost:7687";
      const user = "neo4j";
      const password = "mosaic33";

      try {
        const driver = neo4j.driver(uri, neo4j.auth.basic(user, password))
        const session = driver.session()

        let result = session.run('MATCH (n) RETURN n LIMIT 1');
        console.log(result.summary().toString());

        if (session.run('MATCH (n) RETURN n LIMIT 1').isOpen() === false){
          throw new Error('Connection to neo4j failed');
        }
        console.log(session.toString())
        session.close();
        //return 'Connection successful';
        console.log("success!");
      } catch (error) {
        document.getElementById('status').textContent = 'Error!';
        throw new Error('Connection to neo4j failed')
      } finally {
        document.getElementById('status').textContent = 'Connected!';
      }
    },
    func(){
      console.log("Test clicked");
    }

  }
}



</script>

<template>
    <router-view />
<!--<div>-->
<!--  <button class="test" @click="handleClick()"></button>-->
<!--</div>-->
<!--  <div class="reg-buttons">-->
<!--      <router-link tag="button" to="/signup">No account? Sign up there</router-link>-->
<!--      <router-link tag="button" to="/reset">Forgot your password?</router-link>-->
<!--      <router-link tag="button" to="/login">Log in</router-link>-->
<!--  </div>-->
<!--  <div id="status">Not connected</div>-->
<!--  <button @click="handleClick()">Test</button>-->
</template>

<style scoped lang="sass">
</style>
