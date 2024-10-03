import React, { useState } from 'react';
import { StyleSheet, View, Text } from 'react-native';
import { TextInput, Card, Button } from 'react-native-paper'; 
import { StatusBar } from 'expo-status-bar';

export default function App() {
  const [number, setNumber] = useState('');
  const [percentage, setPercentage] = useState('');
  const [timestamps1, setTimestamps1] = useState('');
  const [timestamps2, setTimestamps2] = useState('');
  const [timestamps3, setTimestamps3] = useState('');
  const [timestamps4, setTimestamps4] = useState('');
  const [timestamps5, setTimestamps5] = useState('');

  return (
    <>
      <View style={styles.app}>      
        <View style={styles.gridContainer}>
          <Card style={styles.card}>
            <Card.Content>
              <Text>Selecione Uma Carta e uma data</Text>
              <TextInput
                label="Digite um número"
                value={number}
                onChangeText={setNumber}
                keyboardType="numeric"
                mode="outlined" 
                style={styles.input}
              />
              <TextInput
                label="Digite o timestamp"
                value={timestamps1}
                onChangeText={setTimestamps1}
                mode="outlined" 
                style={styles.input}
              />
            </Card.Content>
            <Button mode="contained" onPress={() => console.log('Número e Timestamp:', number, timestamps1)} style={styles.button}>
            procurar
          </Button>
          </Card>

          <Card style={styles.card}>
            <Card.Content>
              <Text>Digite a porcentagem desejada e a data</Text>
              <TextInput
                label="Digite uma porcentagem"
                value={percentage}
                onChangeText={setPercentage}
                keyboardType="numeric"
                mode="outlined"
                style={styles.input}
              />
              <TextInput
                label="Digite o timestamp"
                value={timestamps2}
                onChangeText={setTimestamps2}
                mode="outlined" 
                style={styles.input}
              />
            </Card.Content>
            <Button mode="contained" onPress={() => console.log('Porcentagem e Timestamp:', percentage, timestamps2)} style={styles.button}>
            procurar
          </Button>
          </Card>

          <Card style={styles.card}>
            <Card.Content>
              <Text>Calcular derrotas com combo de cartas</Text>
              <TextInput
                label="Digite um número"
                value={number}
                onChangeText={setNumber}
                keyboardType="numeric"
                mode="outlined"
                style={styles.input}
              />
              <TextInput
                label="Digite o timestamp"
                value={timestamps3}
                onChangeText={setTimestamps3}
                mode="outlined" 
                style={styles.input}
              />
            </Card.Content>
            <Button mode="contained" onPress={() => console.log('Número e Timestamp:', number, timestamps3)} style={styles.button}>
            procurar
          </Button>
          </Card>

          <Card style={styles.card}>
            <Card.Content>
              <Text>Vitórias com menos troféus e duas torres derrubadas</Text>
              <TextInput
                label="Digite um número"
                value={number}
                onChangeText={setNumber}
                keyboardType="numeric"
                mode="outlined"
                style={styles.input}
              />
              <TextInput
                label="Digite o timestamp"
                value={timestamps4}
                onChangeText={setTimestamps4}
                mode="outlined" 
                style={styles.input}
              />
            </Card.Content>
            <Button mode="contained" onPress={() => console.log('Número e Timestamp:', number, timestamps4)} style={styles.button}>
            procurar
          </Button>
          </Card>

          <Card style={styles.card}>
            <Card.Content>
              <Text>Combos de cartas que geram vitórias</Text>
              <TextInput
                label="Digite um número"
                value={number}
                onChangeText={setNumber}
                keyboardType="numeric"
                mode="outlined"
                style={styles.input}
              />
              <TextInput
                label="Digite o timestamp"
                value={timestamps5}
                onChangeText={setTimestamps5}
                mode="outlined" 
                style={styles.input}
              />
            </Card.Content>
            <Button mode="contained" onPress={() => console.log('Número e Timestamp:', number, timestamps5)} style={styles.button}>
            procurar
          </Button>
          </Card>         
        </View>
      </View>
    </>
  );
}

const styles = StyleSheet.create({
  app: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100%',
    padding: '5%'
  },
  gridContainer: { 
    flexDirection: 'row',          
    flexWrap: 'wrap',              
    justifyContent: 'center', 
    width: '100%',                
    paddingHorizontal: 10,      
  },
  card: {
    width: '45%',
    marginVertical: '2%',
    marginHorizontal: '2%',
    padding: 10,
  },
  input: {
    marginVertical: 10,
  },
  button: {
    marginTop: 20,
    width: '60%',
    alignSelf: 'center'
  }
});