import React, { Component } from 'react'
import Response from '../Response'
import headers from '../../utils/Headers'
import ServerError from '../../ServerError'

class Monitor extends Component {
  constructor () {
    super()
    // order_of_training_data = ['Screen Technology', 'Comparitive Energy Consumption', 'Active Standby Power']
    // specifications = ['LCD (LED)', 100, 0.35]
    this.state = {
      screenTechnology: 'LCD',
      comparitiveEnergyConsumption: '',
      activeStandbyPower: '',
      response: '',
      loading: false,
      serverError: false
    }
    this.handleChange = this.handleChange.bind(this)
    this.submitForm = this.submitForm.bind(this)
  }
  handleChange (event) {
    event.preventDefault()
    this.setState({ [event.target.name]: event.target.value })
  }
  submitForm (e) {
    this.setState({ loading: true })
    const data = [
      this.state.screenTechnology,
      parseInt(this.state.comparitiveEnergyConsumption),
      parseFloat(this.state.activeStandbyPower)
    ]
    // if (data.includes(NaN) || data.includes('')) {
    //   alert('Fill all Fields')
    //   this.setState({
    //     loading: false
    //   })
    //   return
    // }
    fetch('/api/predict/monitor', {
      method: 'POST',
      mode: 'cors',
      cache: 'no-cache',
      credentials: 'same-origin',
      headers: headers,
      redirect: 'follow',
      referrer: 'no-referrer',
      body: JSON.stringify({
        specifications: data
      })
    })
      .then(response => response.json())
      .then(res => {
        this.setState({
          response: {
            category: res.category,
            info: res.info,
            inference: res.text,
            correlatedParameters: res.correlatedParameters,
            starRange: res.starRange,
            links: res.links,
            idealEnergy: res.idealEnergy
          }
        })
      })
      .catch(() => {
        this.setState({ serverError: true })
      })
  }

  render () {
    var content
    const formContent = (
      <div>
        <div className='container-fluid mb-5 display-4'>
          Tell us about your Monitor
        </div>
        <form className='container w-50'>
          <div className='form-group'>
            <label className='form-inline'>Screen Technology</label>
            <select
              className='form-control'
              name='screenTechnology'
              value={this.state.screenTechnology}
              onChange={this.handleChange}
            >
              <option value='LCD'>LCD</option>
              <option value='LCD (LED)'>LCD (LED)</option>
              <option value='OLED'>OLED</option>
            </select>
          </div>

          <div className='form-group'>
            <label for='comparitiveEnergyConsumption' className='form-inline'>
              Current Comparitive Energy Consumption
            </label>
            <input
              type='number'
              id='comparitiveEnergyConsumption'
              className='form-control'
              placeholder='Comparative Energy Consumption expressed as kilowatt hours per years'
              name='comparitiveEnergyConsumption'
              value={this.state.comparitiveEnergyConsumption}
              onChange={this.handleChange}
              required
            />
          </div>

          <div className='form-group'>
            <label for='activeStandbyPower' className='form-inline'>
              Active Standby Power
            </label>
            <input
              type='number'
              id='activeStandbyPower'
              className='form-control'
              placeholder='Amount of energy used by the monitor in Active Standby Mode in watts'
              name='activeStandbyPower'
              value={this.state.activeStandbyPower}
              onChange={this.handleChange}
              min='0'
              max='10'
              required
            />
          </div>
          <div className='form-group'>
            <input
              type='submit'
              className='submit btn btn-success'
              onClick={this.submitForm}
              disabled={this.state.loading}
            >
              {!this.state.loading ? 'Find Star Rating' : 'Submitting...'}
            </input>
            <button
              type='reset'
              className='form-group btn btn-info ml-3'
              onClick={() => {
                window.location.href = '/'
              }}
            >
              Back to Home
            </button>
          </div>
        </form>
      </div>
    )

    if (this.state.response) {
      content = <Response response={this.state.response} appliance='monitor' />
    } else if (this.state.serverError) {
      content = <ServerError />
    } else content = formContent
    return <div>{content}</div>
  }
}

export default Monitor
