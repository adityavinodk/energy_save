import React, { Component } from 'react'
import Response from '../Response'
import headers from '../../utils/Headers'
import ServerError from '../../ServerError'

class Dryer extends Component {
  constructor () {
    super()
    // specifications = ['AS/NZS 2442.2:2000/Amdt 2:2007 (Legacy)', 'ASKO', 8, True, 'Timer', 'Slovenia', 890, 650, 200, 'Heat and dry', 230, 'Vented', 650]
    // order_of_training_data = ['Appliance Standard', 'Brand', 'Capacity', 'Combination', 'Control', 'Country', 'Depth','Height', 'Current Comparitive Energy Consumption', 'Program Name', 'Program Time', 'Type', 'Width']
    this.state = {
      combination: true,
      control: 'Timer',
      comparitiveEnergyConsumption: '',
      programTime: '',
      type: 'Vented',
      response: '',
      loading: false,
      serverError: false
    }
    this.handleChange = this.handleChange.bind(this)
    this.handleCombination = this.handleCombination.bind(this)
    this.submitForm = this.submitForm.bind(this)
  }
  handleChange (event) {
    event.preventDefault()
    this.setState({ [event.target.name]: event.target.value })
  }
  handleCombination (event) {
    event.preventDefault()
    var value

    var combination = this.state.Combination
    if (combination === 'true') {
      value = true
    } else value = false
    this.setState({ combination: value })
  }
  submitForm (e) {
    e.preventDefault()
    this.setState({ loading: true })
    const data = [
      JSON.parse(this.state.combination),
      this.state.control,
      parseInt(this.state.comparitiveEnergyConsumption),
      parseInt(this.state.programTime),
      this.state.type
    ]

    fetch('/api/predict/dryer', {
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
          Tell us about your Dryer
        </div>
        <form className='container w-50' onSubmit={this.submitForm}>
          <div className='form-group'>
            <label for='combination' className='form-inline'>Combination - washer+dryer?</label>
            <select
              className='form-control'
              id='combination'
              name='combination'
              value={this.state.combination}
              onChange={this.handleChange}
              required
            >
              <option value='true'>True</option>
              <option value='false'>False</option>
            </select>
          </div>

          <div className='form-group'>
            <label className='form-inline'>Control</label>
            <select
              className='form-control'
              name='control'
              value={this.state.control}
              onChange={this.handleChange}
            >
              <option value='Timer'>Timer</option>
              <option value='Autosensing'>Autosensing</option>
              <option value='Manual'>Manual</option>
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
              placeholder='Energy Consumption of the product expressed as kilowatt hours per years'
              name='comparitiveEnergyConsumption'
              value={this.state.comparitiveEnergyConsumption}
              onChange={this.handleChange}
              required
            />
          </div>

          <div className='form-group'>
            <label for='programTime' className='form-inline'>Program Time</label>
            <input
              type='number'
              id='programTime'
              className='form-control'
              placeholder='Program time in minutes'
              name='programTime'
              value={this.state.programTime}
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
              <option value='Vented'>Vented</option>
              <option value='Condenser'>Condenser</option>
            </select>
          </div>
          <button
            type='submit'
            className='btn btn-success'
            disabled={this.state.loading}
          >
            {!this.state.loading ? 'Find Star Rating' : 'Submitting...'}
          </button>
          <button
            type='reset'
            className='btn btn-info ml-3'
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
      content = <Response response={this.state.response} appliance='dryer' />
    } else if (this.state.serverError) {
      content = <ServerError />
    } else content = formContent
    return <div>{content}</div>
  }
}

export default Dryer
