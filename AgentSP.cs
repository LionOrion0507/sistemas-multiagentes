using System.Collections;
using System.Collections.Generic;
using System;
using System.IO;
using System.Text;
using UnityEngine;
using Random = UnityEngine.Random;

public class AgentSP : MonoBehaviour
{
    [SerializeField] private GameObject[] _itemPrefab;
    private GameObject clone;
    private Vector3 spawnPosition;
    private int num;

    // Start is called before the first frame update
    void Start()
    {
        string [,] arr = new string[100, 100];
        string[] arrStr = new string[100];
        
        var path = "Assets/Script/initialPos.txt";
        string[] lines = File.ReadAllLines(path, Encoding.UTF8);

        int ind = 0;
        foreach (string line in lines){
            arrStr[ind] = line;
            ind++;
        }

        Debug.Log("Arr length: " + ind);

        string temp = "";
        for(int i = 0; i<ind; i++){
            temp = arrStr[i];
            string[] words = temp.Split(' ');
            arr[i, 0] = words[0];
            arr[i, 1] = words[1];
            
        }

        StartCoroutine(agentSpawner(arr, ind));
        StartCoroutine(Movement(ind));
    }

    IEnumerator agentSpawner(string[,] arr, int n){
        num = 0;
        
        while (num < n){
            yield return new WaitForSeconds(2);
            
            spawnPosition = new Vector3((float)Convert.ToDouble(arr[num, 0]), 0, (float)Convert.ToDouble(arr[num, 1]));
            if (arr[num, 0] == "30")
            {
                clone = Instantiate(_itemPrefab[1]);
                spawnPosition = new Vector3(((float)Convert.ToDouble(arr[num, 0])), 0, (float)Convert.ToDouble(arr[num, 1]));
                clone.transform.position = spawnPosition;
                clone.name = "Carro " + num.ToString();
            }
            else if (arr[num, 0] == "34")
            {
                clone = Instantiate(_itemPrefab[1]);
                clone.transform.position = spawnPosition;
                clone.name = "Carro " + num.ToString();
            }
            else
            {
                clone = Instantiate(_itemPrefab[0]);
                clone.transform.position = new Vector3((float)Convert.ToDouble(arr[num, 0]), 0, (float)Convert.ToDouble(arr[num, 1]));
                clone.name = "Carro " + num.ToString();
            }
            num++;
        }
    }

    IEnumerator Movement(int carCount)
    {
        string [,] arr = new string[1000, 1000];
        string[] arrStr = new string[1000];

        var path = "Assets/Script/positionsSimul.txt";
        string[] lines = File.ReadAllLines(path, Encoding.UTF8);

        int ind = 0;
        foreach (string line in lines){
            arrStr[ind] = line;
            ind++;
        }

        Debug.Log("Arr length: " + ind);

        string temp = "";
        for(int i = 0; i<ind; i++){
            temp = arrStr[i];
            string[] words = temp.Split(' ');
            arr[i, 0] = words[0];
            arr[i, 1] = words[1];
            
        }

        int cont = 0;
        for (int i = 0; i < ind; i++) {
            yield return new WaitForSeconds(2);
            if (cont == (carCount)){
                cont = 0;
            }
            GameObject aux = GameObject.Find("Carro " + cont.ToString());
            aux.transform.position = new Vector3((float)Convert.ToDouble(arr[i, 0]), 0f, (float)Convert.ToDouble(arr[i, 1]));
            cont++;
        }
    }
}
