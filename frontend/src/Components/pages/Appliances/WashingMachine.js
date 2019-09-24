import React, { Component } from 'react'
import Response from '../Response'
import headers from '../../utils/Headers'
import ServerError from '../../ServerError'

class WashingMachine extends Component {
  constructor () {
    super()
    // order_of_training_data = ['Cap', 'CEC_', 'Conn_Mode', 'delayStartMode', 'internal_heater', 'standbyPowerUsage', 'Type', 'Program Time']
    // specifications = [9, 450, "Dual", true, "Yes", 0.8, "Non-Drum", 150]
    this.state = {
      cap: '',
      cecWarm: '',
      connMode: 'Dual',
      delayStartMode: true,
      internalHeater: 'Yes',
      standbyPowerUsage: '',
      type: 'Drum',
      progTime: '',
      response: '',
      loading: false,
      serverError: false
    }
    this.handleChange = this.handleChange.bind(this)
    this.submitForm = this.submitForm.bind(this)
    this.handleBoolean = this.handleBoolean.bind(this)
  }
  handleChange (event) {
    event.preventDefault()
    this.setState({ [event.target.name]: event.target.value })
  }
  handleBoolean (event) {
    event.preventDefault()
    var value

    var combination = event.target.name
    if (combination === 'true') {
      value = true
    } else value = false
    this.setState({ [event.target.name]: value })
  }
  submitForm (e) {
    e.preventDefault()
    this.setState({ loading: true })
    const data = [
      parseInt(this.state.cap),
      parseInt(this.state.cecWarm),
      this.state.connMode,
      this.state.delayStartMode,
      this.state.internalHeater,
      parseFloat(this.state.standbyPowerUsage),
      this.state.type,
      parseInt(this.state.progTime)
    ]

    fetch('/api/predict/washing_machine', {
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
          Tell us about your Washing Machine
        </div>
        <form className='container w-50' onSubmit={this.submitForm}>
          <div className='form-group'>
            <label for='cap' className='form-inline'>Capacity</label>
            <input
              type='number'
              id='cap'
              className='form-control'
              placeholder='Enter value in kg'
              name='cap'
              value={this.state.cap}
              onChange={this.handleChange}
              required
            />
          </div>

          <div className='form-group'>
            <label for='cecWarm' className='form-inline'>
              Current Comparitive Energy Consumption for Warm Use
            </label>
            <input
              type='number'
              id='cecWarm'
              className='form-control'
              placeholder='Energy Consumption of the product expressed as kilowatt hours per years'
              name='cecWarm'
              value={this.state.cecWarm}
              onChange={this.handleChange}
              required
            />
          </div>

          <div className='form-group'>
            <label className='form-inline'>Connection Mode</label>
            <select
              className='form-control'
              name='connMode'
              value={this.state.connMode}
              onChange={this.handleChange}
            >
              <option value='Dual'>Dual</option>
              <option value='Cold'>Cold</option>
            </select>
          </div>

          <div className='form-group'>
            <label className='form-inline'>Delay Start Mode</label>
            <select
              className='form-control'
              name='delayStartMode'
              value={this.state.delayStartMode}
              onChange={this.handleBoolean}
            >
              <option value='true'>True</option>
              <option value='false'>False</option>
            </select>
          </div>

          <div className='form-group'>
            <label className='form-inline'>Internal Heater?</label>
            <select
              className='form-control'
              name='internalHeater'
              value={this.state.internalHeater}
              onChange={this.handleChange}
            >
              <option value='Yes'>Yes</option>
              <option value='No'>No</option>
            </select>
          </div>

          <div className='form-group'>
            <label for='standbyPowerUsage' className='form-inline'>Standby Power Usage</label>
            <input
              type='text'
              id='standbyPowerUsage'
              className='form-control'
              placeholder='Enter value in watts'
              name='standbyPowerUsage'
              value={this.state.standbyPowerUsage}
              onChange={this.handleChange}
              required
            />
          </div>

          <div className='form-group'>
            <label className='form-inline'>Type</label>
            <select
              className='form-control'
              name='type'
              value={this.state.type}
              onChange={this.handleChange}
            >
              <option value='Drum'>Drum</option>
              <option value='Non-Drum'>Non-Drum</option>
            </select>
          </div>

          <div className='form-group'>
            <label for='progTime' className='form-inline'>Program Time</label>
            <input
              type='number'
              id='progTime'
              className='form-control'
              placeholder='Enter time in minutes'
              name='progTime'
              value={this.state.progTime}
              onChange={this.handleChange}
              required
            />
          </div>

          <button
            type='submit'
            className='form-group btn btn-success'
            disabled={this.state.loading}
          >
            {!this.state.loading ? 'Find Star Rating' : 'Submitting...'}
          </button>
          <button
            type='reset'
            className='form-group btn btn-info ml-3'
            onClick={() => {
              window.location.href = '/'
            }}
          >
            Back to Home
          </button>
        </form>
      </div>
    )

    if (this.state.response) {
      content = (
        <Response response={this.state.response} appliance='washing_machine' />
      )
    } else if (this.state.serverError) {
      content = <ServerError />
    } else content = formContent
    return <div>{content}</div>
  }
}

export default WashingMachine
