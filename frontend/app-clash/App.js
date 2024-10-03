import React, { useState } from 'react';
import { StyleSheet, View, Text } from 'react-native';
import { TextInput, Card, Button } from 'react-native-paper'; 
import { StatusBar } from 'expo-status-bar';

export default function App() {
  const [number, setNumber] = useState('');

  return (
    <>
      <View style={styles.app}>
        
        <View style={styles.gridContainer}>
                   
          <Card style={styles.card}>
            <Card.Content>
              <Text>projeto clash!!!</Text>
              <TextInput
                label="Digite um número"
                value={number}
                onChangeText={setNumber}
                keyboardType="numeric"
                mode="outlined" 
                style={styles.input}
              />a
            </Card.Content>
            <Button mode="contained" onPress={() => console.log('Número digitado:', number)} style={styles.button}>
            Enviar
          </Button>
          </Card>

          <Card style={styles.card}>
            <Card.Content>
              <Text>projeto clash!!!</Text>
              <TextInput
                label="Digite um número"
                value={number}
                onChangeText={setNumber}
                keyboardType="numeric"
                mode="outlined"
                style={styles.input}
              />
            </Card.Content>
            <Button mode="contained" onPress={() => console.log('Número digitado:', number)} style={styles.button}>
            Enviar
          </Button>
          </Card>

          <Card style={styles.card}>
            <Card.Content>
              <Text>projeto clash!!!</Text>
              <TextInput
                label="Digite um número"
                value={number}
                onChangeText={setNumber}
                keyboardType="numeric"
                mode="outlined"
                style={styles.input}
              />
            </Card.Content>
            <Button mode="contained" onPress={() => console.log('Número digitado:', number)} style={styles.button}>
            Enviar
          </Button>
          </Card>


          <Card style={styles.card}>
            <Card.Content>
              <Text>projeto clash!!!</Text>
              <TextInput
                label="Digite um número"
                value={number}
                onChangeText={setNumber}
                keyboardType="numeric"
                mode="outlined"
                style={styles.input}
              />
            </Card.Content>
            <Button mode="contained" onPress={() => console.log('Número digitado:', number)} style={styles.button}>
            Enviar
          </Button>
          </Card>

          <Card style={styles.card}>
            <Card.Content>
              <Text>projeto clash!!!</Text>
              <TextInput
                label="Digite um número"
                value={number}
                onChangeText={setNumber}
                keyboardType="numeric"
                mode="outlined"
                style={styles.input}
              />
            </Card.Content>
            <Button mode="contained" onPress={() => console.log('Número digitado:', number)} style={styles.button}>
            Enviar
          </Button>
          </Card>

          <Card style={styles.card}>
            <Card.Content>
              <Text>projeto clash!!!</Text>
              <TextInput
                label="Digite um número"
                value={number}
                onChangeText={setNumber}
                keyboardType="numeric"
                mode="outlined"
                style={styles.input}
              />
            </Card.Content>
            <Button mode="contained" onPress={() => console.log('Número digitado:', number)} style={styles.button}>
            Enviar
          </Button>
          </Card>
          <Card style={styles.card}>
            <Card.Content>
              <Text>projeto clash!!!</Text>
              <TextInput
                label="Digite um número"
                value={number}
                onChangeText={setNumber}
                keyboardType="numeric"
                mode="outlined"
                style={styles.input}
              />
            </Card.Content>
            <Button mode="contained" onPress={() => console.log('Número digitado:', number)} style={styles.button}>
            Enviar
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
