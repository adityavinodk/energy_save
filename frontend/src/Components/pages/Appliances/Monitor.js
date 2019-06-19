import React, { Component } from 'react';
import headers from '../../utils/Headers';

class Monitor extends Component {
  constructor() {
    super();
    // order_of_training_data = ['Screen Technology', 'Comparitive Energy Consumption', 'Active Standby Power']
    // specifications = ['LCD (LED)', 100, 0.35]
    this.state = {
      'screenTechnology':'LCD',
      'comparitiveEnergyConsumption':'',
      'activeStandbyPower': ''
    }
    this.handleChange = this.handleChange.bind(this);
    this.handleTech = this.handleTech.bind(this);
    this.submitForm = this.submitForm.bind(this);
  }
  handleChange(event) {
    event.preventDefault();
    this.setState({ [event.target.name] : event.target.value });
  }
  handleTech(event){
    event.preventDefault();
    this.setState({'screenTechnology': event.target.value});
  }
  submitForm(e) {
    e.preventDefault();
    const data = [
        this.state.screenTechnology,
        parseInt(this.state.comparitiveEnergyConsumption),
        parseInt(this.state.activeStandbyPower)
    ];
    // console.log(data);
    fetch('http://localhost:5000/api/predict/monitor', {
      method: 'POST',
      mode: 'cors',
      cache: 'no-cache',
      credentials: 'same-origin',
      headers: headers,
      redirect: 'follow',
      referrer: 'no-referrer',
      body: JSON.stringify({
        "specifications": data
      }),
    })
      .then(response => response.json())
      .then(res => {
        console.log(res);
        this.setState({ response: res })
      })
  }
  render() {
    return (
      <div>
        <div className="container-fluid mb-5 display-4">
          Monitor Details
        </div>
        <form className="container w-50">

            <div className="form-group">
              <label className="form-inline">Screen Technology</label>
              <select
                className="form-control"
                name='screenTechnology'
                value={this.state.screenTechnology}
                onChange={this.handleTech}
              >
                <option value="LCD">LCD</option>
                <option value="LCD (LED)">LCD (LED)</option>
                <option value="OLED">OLED</option>
              </select>
            </div>

            <div className="form-group">
                <label className="form-inline">Current Comparitive Energy Consumption</label>
                <input
                type='text'
                className="form-control"
                placeholder='Enter the Comparative Energy Consumption of the product expressed as kilowatt hours per years'
                name='comparitiveEnergyConsumption'
                value={this.state.comparitiveEnergyConsumption}
                onChange={this.handleChange}
                />
            </div>

            <div className="form-group">
                <label className="form-inline">Active Standby Power</label>
                <input
                type='number'
                className="form-control"
                placeholder='Enter the amount of energy used by the monitor in Active Standby Mode'
                name='activeStandbyPower'
                value={this.state.activeStandbyPower}
                onChange={this.handleChange}
                />
            </div>
            <button
                type='submit'
                className='form-group btn btn-lg btn-success'
                onClick={this.submitForm}
            >
            Find Star Rating
          </button>
        </form>
      </div>

    );
  }
}

export default Monitor;