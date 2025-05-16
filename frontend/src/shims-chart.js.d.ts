declare module 'chart.js/auto' {
  import { Chart } from 'chart.js';
  export default Chart;
}

// Ampliar interfaces para evitar errores de tipo
declare module 'chart.js' {
  interface TooltipCallbacks {
    label?: (context: any) => string | string[];
    title?: (context: any) => string | string[];
  }
  
  interface Dataset {
    data?: any[];
    label?: string;
    backgroundColor?: string | ((context: any) => string);
    width?: any;
    height?: any;
  }
  
  interface ChartDataset {
    data?: any[];
    backgroundColor?: string | ((context: any) => string);
    width?: any;
    height?: any;
  }
  
  interface ScaleOptions {
    y?: any;
    x?: any;
  }
} 