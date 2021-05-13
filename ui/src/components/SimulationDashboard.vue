<template>
  <div class="mx-5">
    <b-card footer-border-variant="light" sub-title="Please fill the query params for the simulation process (all time must be in minutes), if not just use the default values!">
      <h4 class="card-title">&#127850; &#127860; Waiters Form - Restaurant Simulation &#x1F374; &#127850;</h4>

      <b-form class="mt-5" @submit="onSubmit" v-if="showForm">
        <b-container>
          <b-row>
            <b-col>
              <b-form-group label="Random Seed:" label-for="random-seed" description="Generic random value, helps to obtain replicable results in the simulation.">
                <b-form-input
                    id="random-seed"
                    v-model.number="form.randomSeed"
                    type="number"
                    size="sm"
                    required
                ></b-form-input>
              </b-form-group>
            </b-col>

            <b-col>
              <b-form-group label="Working days:" label-for="working-days">
                <b-form-input
                    id="working-days"
                    v-model.number="form.workingDays"
                    type="number"
                    size="sm"
                    required
                ></b-form-input>
              </b-form-group>
            </b-col>

            <b-col>
              <b-form-group label="Working hours:" label-for="working-hours">
                <b-form-input
                    id="working-hours"
                    v-model.number="form.workingHours"
                    type="number"
                    size="sm"
                    required
                ></b-form-input>
              </b-form-group>
            </b-col>
          </b-row>

          <b-row>
            <b-col>
              <b-form-group label="Workers:" label-for="workers" description="Persons to start working in the restaurant process.">
                <b-form-input
                    id="workers"
                    v-model.number="form.workers"
                    type="number"
                    size="sm"
                    required
                ></b-form-input>
              </b-form-group>
            </b-col>

            <b-col>
              <b-form-group label="Work count:" label-for="work-count" description="Determines the number of simultaneous work per stage.">
                <b-form-input
                    id="work-count"
                    v-model.number="form.workCount"
                    type="number"
                    size="sm"
                    required
                ></b-form-input>
              </b-form-group>
            </b-col>
          </b-row>

          <hr>
          <h5>Times for simulation steps &#127828; &#127829;</h5>
          <br>

          <b-row>
            <b-col>
              <b-form-group label="Go to table time:" label-for="goToTable">
                <b-form-input
                    id="goToTable"
                    v-model.number="form.times.goToTable"
                    type="number"
                    size="sm"
                    required
                ></b-form-input>
              </b-form-group>
            </b-col>

            <b-col>
              <b-form-group label="Go to kitchen time:" label-for="goToKitchen">
                <b-form-input
                    id="goToKitchen"
                    v-model.number="form.times.goToKitchen"
                    type="number"
                    size="sm"
                    required
                ></b-form-input>
              </b-form-group>
            </b-col>
          </b-row>

          <b-row>
            <b-col>
              <b-form-group label="Bring menu time:" label-for="bringMenu">
                <b-form-input
                    id="bringMenu"
                    v-model.number="form.times.bringMenu"
                    type="number"
                    size="sm"
                    required
                ></b-form-input>
              </b-form-group>
            </b-col>

            <b-col>
              <b-form-group label="Take order time:" label-for="takeOrder">
                <b-form-input
                    id="takeOrder"
                    v-model.number="form.times.takeOrder"
                    type="number"
                    size="sm"
                    required
                ></b-form-input>
              </b-form-group>
            </b-col>
          </b-row>

          <b-row>
            <b-col>
              <b-form-group label="Send order to kitchen time:" label-for="sendOrder">
                <b-form-input
                    id="sendOrder"
                    v-model.number="form.times.sendOrder"
                    type="number"
                    size="sm"
                    required
                ></b-form-input>
              </b-form-group>
            </b-col>

            <b-col>
              <b-form-group label="Serve table time:" label-for="serveTable">
                <b-form-input
                    id="serveTable"
                    v-model.number="form.times.serveTable"
                    type="number"
                    size="sm"
                    required
                ></b-form-input>
              </b-form-group>
            </b-col>
          </b-row>

          <b-row>
            <b-col>
              <b-form-group label="Rest interval time:" label-for="restInterval">
                <b-form-input
                    id="restInterval"
                    v-model.number="form.times.restInterval"
                    type="number"
                    size="sm"
                    required
                ></b-form-input>
              </b-form-group>
            </b-col>

            <b-col>
              <b-form-group label="Rest time:" label-for="rest">
                <b-form-input
                    id="rest"
                    v-model.number="form.times.rest"
                    type="number"
                    size="sm"
                    required
                ></b-form-input>
              </b-form-group>
            </b-col>
          </b-row>

          <b-row>
            <b-col cols="6">
              <b-form-group label="Clean time:" label-for="clean">
                <b-form-input
                    id="clean"
                    v-model.number="form.times.clean"
                    type="number"
                    size="sm"
                    required
                ></b-form-input>
              </b-form-group>
            </b-col>
          </b-row>
        </b-container>

        <br>

        <div class="custom-container">
          <b-button type="submit" variant="primary">Submit</b-button>
        </div>
      </b-form>
    </b-card>

    <b-modal ref="results" hide-footer size="xl" title="Simulation results">
      <b-list-group class="mt-3">
        <b-list-group-item v-for="(line, index) in results.flowLogs" v-bind:key="index">
          {{ line }}
        </b-list-group-item>
      </b-list-group>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: 'SimulationDashboard',
  data() {
    return {
      form: {
        workingDays: 1,
        workingHours: 8,
        randomSeed: 45,
        workers: 3,
        workCount: 3,
        times: {
          goToTable: 1,
          goToKitchen: 2,
          bringMenu: 1,
          takeOrder: 3,
          sendOrder: 1,
          serveTable: 3,
          restInterval: 120,
          rest: 10,
          clean: 2
        }
      },
      showForm: true,
      results: {
        flowLogs: [],
        lotTimes: []
      }
    }
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();
      axios
          .post('http://localhost:5000/simulate/', this.form)
          .then(response => {
            this.results = response.data;
            this.results.lotTimes = this.results.lotTimes.sort((a, b) => parseFloat(a) - parseFloat(b));
            this.results.lotTimes = this.results.lotTimes.map(number => this.convertToHours(number));
            this.$refs['results'].show();
          })
          .catch(error => console.log(error))
    },
    convertToHours(time) {
      let hours = Math.floor(time / 60);
      let minutes = time % 60;
      let day = Math.floor(hours / 8);
      return `${hours} hours with ${minutes} minutes (${day} production day - ${time} production minutes).`;
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.card-title, .card-subtitle, .custom-container {
  text-align: center;
}
.list-group{
  max-height: 300px;
  margin-bottom: 10px;
  overflow:scroll;
  -webkit-overflow-scrolling: touch;
}
button {
  width: 25%;
}
</style>